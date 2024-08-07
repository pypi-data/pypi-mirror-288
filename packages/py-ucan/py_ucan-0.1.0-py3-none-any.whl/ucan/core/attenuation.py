from __future__ import annotations

import typing as t
import typing_extensions as te

from ucan.core.capability import Ability, Capability, ResourcePointer
from ucan.core.plugins import Plugins
from ucan.core.token import validate_proofs
from ucan.core.types import IsRevokedFunc, Ucan
from ucan.schemas import BaseModel, validate_call


@te.runtime_checkable
class _CanDelegateResourceFunc(te.Protocol):
    async def __call__(
        self, parent_resource: ResourcePointer, child_resource: ResourcePointer
    ) -> bool: ...


@te.runtime_checkable
class _CanDelegateAbilityFunc(te.Protocol):
    async def __call__(
        self, parent_ability: Ability, child_ability: Ability
    ) -> bool: ...


@te.runtime_checkable
class DelegationChainsFunc(te.Protocol):
    def __call__(
        self,
        semantics: DelegationSemantics,
        ucan: Ucan,
        is_revoked: IsRevokedFunc,
    ) -> te.AsyncIterator[Exception | DelegationChain]: ...


class DelegationSemantics(te.NamedTuple):
    can_delegate_resource: _CanDelegateResourceFunc
    """
    * Whether a parent resource can delegate a child resource.
    *
    * An implementation may for example decide to return true for
    * `can_delegate_resource(
        ResourcePointer.decode("path:/parent/"),
        ResourcePointer.decode("path:/parent/child/"),
        )`
    """
    can_delegate_ability: _CanDelegateAbilityFunc
    """
    * Whether a parent ability can delegate a child ability.
    *
    * An implementation may for example decide to return true for
    * `can_delegate_ability(
        Ability.decode("crud/UPDATE"),
        Ability.decode("crud/CREATE"),
        )`
    """


class DelegatedCapability(BaseModel):
    capability: Capability
    ucan: Ucan
    chain_step: DelegatedCapability | None = None


DelegationChain = DelegatedCapability


async def _default_can_delegate_resource(
    parent_resource: ResourcePointer, child_resource: ResourcePointer
) -> bool:
    if parent_resource.scheme != child_resource.scheme:
        return False

    return parent_resource.hier_part == child_resource.hier_part


async def _default_can_delegate_ability(
    parent_ability: Ability, child_ability: Ability
) -> bool:
    if parent_ability == "SUPERUSER":
        return True

    if child_ability == "SUPERUSER":
        return False

    if parent_ability.namespace != child_ability.namespace:
        return False

    # Array equality
    if len(parent_ability.segments) != len(child_ability.segments):
        return False

    acc = True
    try:
        for idx, value in enumerate(parent_ability.segments):
            acc = acc and child_ability.segments[idx] == value

    except IndexError:
        acc = False

    return acc


equal_can_delegate: DelegationSemantics = DelegationSemantics(
    can_delegate_resource=_default_can_delegate_resource,
    can_delegate_ability=_default_can_delegate_ability,
)


async def capability_can_be_delegated(
    semantics: DelegationSemantics,
    capability: Capability,
    from_delegation_chain: DelegationChain,
) -> bool:
    return await _can_delegate(semantics, from_delegation_chain.capability, capability)


@validate_call
def delegation_chains(plugins: Plugins) -> DelegationChainsFunc:
    """Compute all possible delegations for given UCAN.

    This computes all possible delegations from given UCAN with given
    capability delegation semantics.

    For each entry in the attenuations array of the UCAN there will be at least
    one delegation chain.

    These delegation chains are computed lazily, so that if parts of the UCAN have
    been revoked or can't be loaded, this doesn't keep this function from figuring
    out different ways of delegating a capability from the attenuations.
    It also makes it possible to return early if a valid delegation chain has been found.

    Args:
        plugins (Plugins): _description_
    """

    @validate_call
    async def _delegation_chains_inner(
        semantics: DelegationSemantics, ucan: Ucan, is_revoked: IsRevokedFunc
    ) -> te.AsyncIterator[Exception | DelegationChain]:
        if await is_revoked(ucan):
            yield Exception(f"UCAN Revoked: {ucan}")

        async for x1 in _capabilities_from_parenthood(ucan):
            yield x1

        async for x2 in _capabilities_from_delegation(
            plugins, semantics, ucan, is_revoked
        ):
            yield x2

    return _delegation_chains_inner


@validate_call
def get_root_issuer(chain: DelegationChain) -> str:
    return (
        chain.ucan.payload.iss
        if chain.chain_step is None
        else get_root_issuer(chain.chain_step)
    )


# Internal API


@validate_call
async def _capabilities_from_parenthood(
    ucan: Ucan,
) -> t.AsyncIterator[DelegationChain]:
    for cap in ucan.payload.att:
        match cap.with_.scheme.lower():
            case _:
                yield DelegationChain(capability=cap, ucan=ucan)


@validate_call
async def _capabilities_from_delegation(
    plugins: Plugins,
    semantics: DelegationSemantics,
    ucan: Ucan,
    is_revoked: IsRevokedFunc,
) -> t.AsyncIterator[Exception | DelegationChain]:
    async for proof in validate_proofs(plugins)(ucan):
        if isinstance(proof, Exception):
            yield proof
            continue

        for cap in ucan.payload.att:
            try:
                waiting: t.AsyncIterator[t.Any]
                match cap.with_.scheme.lower():
                    case _:
                        waiting = _handle_normal_delegation(
                            plugins, semantics, cap, ucan, proof, is_revoked
                        )

                async for x in waiting:
                    yield x

            except Exception as e:  # noqa: PERF203
                yield e


@validate_call
async def _handle_normal_delegation(
    plugins: Plugins,
    semantics: DelegationSemantics,
    capability: Capability,
    ucan: Ucan,
    proof: Ucan,
    is_revoked: IsRevokedFunc,
) -> t.AsyncIterator[Exception | DelegationChain]:
    async for chain in delegation_chains(plugins)(semantics, proof, is_revoked):
        if isinstance(chain, Exception):
            yield chain
            continue

        if not await capability_can_be_delegated(semantics, capability, chain):
            continue

        yield DelegationChain(capability=capability, ucan=ucan, chain_step=chain)


@validate_call
async def _can_delegate(
    semantics: DelegationSemantics,
    parent_capability: Capability,
    child_capability: Capability,
) -> bool:
    return await semantics.can_delegate_resource(
        parent_capability.with_, child_capability.with_
    ) and await semantics.can_delegate_ability(
        parent_capability.can, child_capability.can
    )
