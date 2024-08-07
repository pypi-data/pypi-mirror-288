from __future__ import annotations

import datetime as dt

import base58

from ucan.constants import PREFIX_DID_BASE58


# datetime helpers


def aware_utcnow() -> dt.datetime:
    """Construct a timezone (UTC) aware datetime."""
    return dt.datetime.now(dt.timezone.utc)


def aware_utcfromtimestamp(timestamp: float) -> dt.datetime:
    """Construct a timezone (UTC) aware datetime from a POSIX timestamp."""
    return dt.datetime.fromtimestamp(timestamp, dt.timezone.utc)


def naive_utcnow() -> dt.datetime:
    """Construct a non-timezone aware datetime in UTC."""
    return aware_utcnow().replace(tzinfo=None)


def naive_utcfromtimestamp(timestamp: float) -> dt.datetime:
    """Construct a non-timezone aware datetime in UTC from a POSIX timestamp."""
    return aware_utcfromtimestamp(timestamp).replace(tzinfo=None)


def isoformat(o: dt.date | dt.time) -> str:
    """Return the date formatted according to ISO."""
    return o.isoformat()


# cryptography helpers


def is_did(data: str) -> bool:
    return data.startswith(PREFIX_DID_BASE58)


def validate_is_did(data: str) -> str:
    if not is_did(data):
        msg = f"Expected a DID strings, but got {data}"
        raise ValueError(msg)

    return data


def has_prefix(data: bytes, prefix: bytes) -> bool:
    """Determines if a Uint8Array has a given indeterminate length-prefix."""
    if data.startswith(prefix):
        return True

    return False


def parse_prefixed_bytes(did: str) -> bytes:
    if not is_did(did):
        raise ValueError(f"Not a valid base58 formatted did:key: {did}")

    did_without_prefix = did[len(PREFIX_DID_BASE58) :]
    return base58.b58decode(did_without_prefix)


def did_from_key_bytes(public_key_bytes: bytes, prefix: bytes) -> str:
    data_bytes = prefix + public_key_bytes
    base58_key = base58.b58encode(data_bytes).decode()
    return PREFIX_DID_BASE58 + base58_key


def did_to_key_bytes(did: str, expected_prefix: bytes) -> bytes:
    data_bytes = parse_prefixed_bytes(did)

    if not has_prefix(data_bytes, expected_prefix):
        msg = f"Expected prefix: {expected_prefix.decode()}"
        raise ValueError(msg)

    return data_bytes[len(expected_prefix) :]
