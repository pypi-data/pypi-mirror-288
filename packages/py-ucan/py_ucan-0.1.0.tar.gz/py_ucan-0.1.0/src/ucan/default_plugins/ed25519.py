from __future__ import annotations

import base64
import typing_extensions as te

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey as PrivateKey,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey as PublicKey,
)

from ucan.constants import PREFIX_DID_ALG_ED25519
from ucan.core.plugins import DidableKey, DidKeyPlugin, ExportableKey
from ucan.schemas import BaseModel
from ucan.utils import did_from_key_bytes, did_to_key_bytes


__all__ = (
    "EdKeypair",
    "ed25519_plugin",
    "ed25519_verify_signature",
)


class EdPublicKeyModel(BaseModel):
    kty: str
    crv: str


class EdPrivateKeyModel(EdPublicKeyModel):
    d: str


class EdKeypair(DidableKey, ExportableKey[EdPrivateKeyModel]):
    jwt_alg = "EdDSA"
    prefix = b"".join(PREFIX_DID_ALG_ED25519)
    # https://github.com/multiformats/multicodec/blob/e9ecf587558964715054a0afcc01f7ace220952c/table.csv#L94

    _private_key: PrivateKey

    @classmethod
    def generate(cls) -> te.Self:
        return cls(PrivateKey.generate())

    @classmethod
    def from_secret_key(cls, data: str) -> te.Self:
        key_bytes = base64.b64decode(data)
        if len(key_bytes) == 64:
            key_bytes = key_bytes[:32]

        if len(key_bytes) != 32:
            raise ValueError("An Ed25519 private key is 32 bytes long")

        return cls(PrivateKey.from_private_bytes(key_bytes))

    @classmethod
    def import_key(cls, data: EdPrivateKeyModel) -> te.Self:
        return cls.from_secret_key(data.d)

    @property
    def public_key(self) -> PublicKey:
        return self._private_key.public_key()

    @property
    def public_key_bytes(self) -> bytes:
        return self.public_key.public_bytes_raw()

    @property
    def _private_key_bytes(self) -> bytes:
        return self._private_key.private_bytes_raw()

    def __init__(self, private_key: PrivateKey) -> None:
        self._private_key = private_key

    def did(self) -> str:
        return did_from_key_bytes(self.public_key_bytes, self.prefix)

    def export(self) -> EdPrivateKeyModel:
        return EdPrivateKeyModel(
            kty="EC",
            crv="Ed25519",
            d=base64.b64encode(self._private_key_bytes).decode(),
        )

    def sign(self, msg: bytes) -> bytes:
        """Sign a message `msg`."""
        return self._private_key.sign(msg)


async def ed25519_verify_signature(did: str, data: bytes, signature: bytes) -> bool:
    public_key_bytes = did_to_key_bytes(did, EdKeypair.prefix)
    public_key = PublicKey.from_public_bytes(public_key_bytes)
    try:
        public_key.verify(signature, data)

    except Exception:
        return False

    return True


ed25519_plugin = DidKeyPlugin(
    jwt_alg=EdKeypair.jwt_alg,
    prefix=EdKeypair.prefix,
    verify_signature=ed25519_verify_signature,
)
