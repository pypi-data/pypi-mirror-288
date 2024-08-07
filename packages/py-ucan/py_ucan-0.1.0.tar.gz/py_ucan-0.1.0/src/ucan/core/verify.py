"""ucans.core.verify module."""

from __future__ import annotations

import typing as t
import typing_extensions as te

from ucan.core import token as tokenlib
from ucan.core.attenuation import (
    capability_can_be_delegated,
    delegation_chains,
    DelegationChain,
    DelegationSemantics,
    equal_can_delegate,
    get_root_issuer,
)
from ucan.core.capability import Capability
from ucan.core.plugins import Plugins
from ucan.core.types import IsRevokedFunc, Ucan
from ucan.schemas import BaseModel, DidString, validate_call


__all__ = (
    # models
    "RequiredCapability",
    "Verification",
    "VerifyResult",
    "VerifyResultError",
    "VerifyResultOk",
    # typing
    "VerifyTokenFunc",
    # utils
    "default_is_revoked",
    "verify",
)


# models


class RequiredCapability(BaseModel):
    capability: Capability
    root_issuer: DidString


class Verification(RequiredCapability):
    proof: DelegationChain


class VerifyResultOk(BaseModel):
    ok: t.Literal[True]
    value: list[Verification]


class VerifyResultError(BaseModel):
    ok: t.Literal[False]
    errors: list[Exception]


VerifyResult = VerifyResultOk | VerifyResultError


# typing


@te.runtime_checkable
class VerifyTokenFunc(te.Protocol):
    """Signature for the `verify` method."""

    async def __call__(
        self,
        encoded_ucan: str,
        audience: DidString,
        required_capabilities: list[RequiredCapability],
        semantics: DelegationSemantics | None = ...,
        is_revoked: IsRevokedFunc | None = ...,
    ) -> VerifyResult: ...


# utils


async def default_is_revoked(ucan: Ucan) -> bool:  # noqa: ARG001
    """Assumes all tokens are valid.

    Args:
        ucan (Ucan): Ucan to check.

    Returns:
        bool: Whether token is revoked.
    """
    return False


@validate_call
def verify(plugins: Plugins) -> VerifyTokenFunc:
    @validate_call
    async def _verify_inner(
        encoded_ucan: str,
        audience: DidString,
        required_capabilities: list[RequiredCapability],
        semantics: DelegationSemantics | None = None,
        is_revoked: IsRevokedFunc | None = None,
    ) -> VerifyResult:
        """Verify a UCAN for an invocation.

        Args:
            encoded_ucan (str): a UCAN to verify for invocation in JWT format.
                (starts with 'eyJ...' and has two '.' in it)
            audience (str): the DID of the callee of this function.
                The expected audience of the outermost level of the UCAN.
                NOTE: This DID should not be hardcoded in production calls
                    to this function.
            required_capabilities (list[RequiredCapability]):
                a non-empty list of capabilities required for this UCAN invocation.
                The root issuer and capability should be derived from something like
                your HTTP request parameters. They identify the resource that's
                access-controlled.
            semantics (DelegationSemantics | None, optional): an optional record of
                functions that specify what the rules for delegating capabilities are.
                If not provided, the default semantics will be `equal_can_delegate`.
                Defaults to None.
            is_revoked (IsRevokedFunc | None, optional): an async predicate on UCANs to
                figure out whether they've been revoked or not. Usually that means
                checking whether the hash of the UCAN is in a list of revoked UCANs.
                If not provided, it will assume no UCAN to be revoked. Defaults to None.
        """
        if is_revoked is None:
            is_revoked = default_is_revoked

        if semantics is None:
            semantics = equal_can_delegate

        if len(required_capabilities) < 1:
            msg = "Expected a non-empty list of required capabilities."
            raise TypeError(msg)

        try:
            # Verify the UCAN
            ucan = await tokenlib.validate(plugins)(encoded_ucan)

            if ucan.payload.aud != audience:
                msg = (
                    f"Invalid UCAN: Expected audience to be {audience}, "
                    f"but it's {ucan.payload.aud}"
                )
                raise ValueError(msg)  # noqa: TRY301

            errors: list[Exception] = []
            proven: list[Verification] = []
            remaining = required_capabilities.copy()
            async for chain_item in delegation_chains(plugins)(
                semantics, ucan, is_revoked
            ):
                if isinstance(chain_item, Exception):
                    errors.append(chain_item)
                    continue

                # Try to look for capabilities from given delegation chain
                for expected in remaining:
                    if (
                        await capability_can_be_delegated(
                            semantics, expected.capability, chain_item
                        )
                        and get_root_issuer(chain_item) == expected.root_issuer
                    ):
                        remaining.remove(expected)
                        proven.append(
                            Verification(
                                capability=expected.capability,
                                root_issuer=expected.root_issuer,
                                proof=chain_item,
                            )
                        )

                # If we've already verified all, we don't need to keep looking
                if not remaining:
                    break

            return (
                VerifyResultError(ok=False, errors=errors)
                if len(remaining) > 0
                else VerifyResultOk(ok=True, value=proven)
            )

        except Exception as e:
            return VerifyResultError(
                ok=False,
                errors=[Exception(f"Unknown error during UCAN verification: {e}")],
            )

    return _verify_inner
