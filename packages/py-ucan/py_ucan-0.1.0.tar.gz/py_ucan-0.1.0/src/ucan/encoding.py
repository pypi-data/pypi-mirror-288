from __future__ import annotations

import typing as t

import jwt


__all__ = ("Base64UrlEncoder",)


class Base64UrlEncoder:
    """URL-safe Base64 encoder."""

    @classmethod
    def decode(cls, data: t.AnyStr) -> bytes:
        """Decode the data from base64 encoded bytes to original bytes data.

        Args:
            data: The data to decode.

        Returns:
            The decoded data.
        """
        try:
            return jwt.utils.base64url_decode(data)

        except ValueError as e:
            msg = f"JWT Base64 decoding error: '{e}'"
            raise ValueError(msg) from e

    @classmethod
    def unverified_decode_complete(cls, data: t.AnyStr) -> dict[str, t.Any]:
        """Decoded an encoded JWT fully without verifying the signature.

        Args:
            data: The data to decode.

        Returns:
            The decoded JWT.
        """
        return jwt.api_jwt.decode_complete(data, options={"verify_signature": False})

    @classmethod
    def validate_encoded(cls, data: str) -> str:
        """Validate an already base64 encoded part of a JWT.

        Args:
            data: The data to validate.

        Returns:
            The same data back.
        """
        cls.decode(data)
        return data

    @classmethod
    def encode(cls, value: bytes) -> bytes:
        """Encode the data from bytes to a base64 encoded bytes.

        Args:
            value: The data to encode.

        Returns:
            The encoded data.
        """
        return jwt.utils.base64url_encode(value)
