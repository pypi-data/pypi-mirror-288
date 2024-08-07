from __future__ import annotations

import abc
import typing as t
import typing_extensions as te

from ucan.schemas import BaseModel, DidString, T_BaseModel, validate_call
from ucan.utils import has_prefix, parse_prefixed_bytes


__all__ = (
    # typing
    "SignatureVerifyFunc",
    # abstract bases
    "Didable",
    "Keypair",
    "DidableKey",
    "ExportableKey",
    "ExportableKey",
)


# typing


@te.runtime_checkable
class SignatureVerifyFunc(te.Protocol):
    async def __call__(self, did: str, data: bytes, signature: bytes) -> bool: ...


# abstract bases


class Didable(abc.ABC):
    @abc.abstractmethod
    def did(self) -> str:
        """Create a DID."""


class Keypair(abc.ABC):
    @property
    @abc.abstractmethod
    def jwt_alg(self) -> str:
        """Algorithm."""

    @abc.abstractmethod
    def sign(self, msg: bytes) -> bytes:
        """Sign a message `msg`."""


class DidableKey(Didable, Keypair):
    @property
    @abc.abstractmethod
    def prefix(self) -> bytes:
        """DID prefix."""


class ExportableKey(abc.ABC, t.Generic[T_BaseModel]):
    @classmethod
    @abc.abstractmethod
    def import_key(cls, data: T_BaseModel) -> te.Self:
        """Import a key."""

    @abc.abstractmethod
    def export(self) -> T_BaseModel:
        """Export a key."""


# plugin


class DidKeyPlugin(BaseModel):
    prefix: bytes
    jwt_alg: str
    # async func(did: str, data: bytes, signature: bytes) -> bool: ...
    verify_signature: SignatureVerifyFunc


class Plugins:
    keys: list[DidKeyPlugin]

    @validate_call
    def __init__(self, keys: list[DidKeyPlugin]) -> None:
        self.keys = keys

    @validate_call
    def _validate_did_method(self, did: DidString) -> str:
        did_method = _parse_did_method(did)
        if did_method != "key":
            msg = f"Unknow did type: {did_method}. Expected 'key'."
            raise ValueError(msg)

        return did_method

    @validate_call
    async def verify_issuer_alg(self, did: DidString, jwt_alg: str) -> bool:
        self._validate_did_method(did)

        prefixed_bytes = parse_prefixed_bytes(did)

        for key_plugin in self.keys:
            if has_prefix(prefixed_bytes, key_plugin.prefix):
                return key_plugin.jwt_alg == jwt_alg

        msg = f"DID method not supported by plugins: {did}"
        raise ValueError(msg)

    @validate_call
    async def verify_signature(
        self, did: DidString, data: bytes, signature: bytes
    ) -> bool:
        self._validate_did_method(did)

        prefixed_bytes = parse_prefixed_bytes(did)

        for key_plugin in self.keys:
            if has_prefix(prefixed_bytes, key_plugin.prefix):
                return await key_plugin.verify_signature(did, data, signature)

        msg = f"DID method not supported by plugins: {did}"
        raise ValueError(msg)


# internal utils


@validate_call
def _parse_did_method(did: DidString) -> str:
    parts = did.split(":")
    if len(parts[1]) < 1:
        raise Exception(f"No DID method included: {did}")

    return parts[1]
