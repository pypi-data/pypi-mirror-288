from __future__ import annotations

import typing as t
import typing_extensions as te

import pydantic as pyd

from ucan.core.capability import Capability
from ucan.core.semver import SemVer
from ucan.encoding import Base64UrlEncoder
from ucan.schemas import BaseModel, JWTBase64Str


# Function types


@te.runtime_checkable
class IsRevokedFunc(te.Protocol):
    """Signature of the function to check whether a token is known to be revoked."""

    async def __call__(self, ucan: Ucan) -> bool: ...  # noqa: D102


# SCHEMAS


class UcanHeader(BaseModel):
    alg: str
    typ: str
    ucv: SemVer

    @pyd.field_validator("ucv", mode="before")
    def validate_ucv(cls, data: str | t.Any) -> SemVer | t.Any:
        if isinstance(data, str):
            return SemVer.decode(data)

        return data


class UcanPayload(BaseModel):
    iss: str
    aud: str
    exp: int
    nbf: int | None = None
    nnc: str | None = None
    att: list[Capability]
    fct: list[t.Any] | None = None
    prf: list[str]


class Ucan(BaseModel):
    """Full UCAN Token model."""

    header: UcanHeader
    payload: UcanPayload
    # We need to keep the encoded version around to preserve the signature
    signed_data: str = pyd.Field(alias="signedData")
    signature: JWTBase64Str

    @property
    def signed_data_bytes(self) -> bytes:
        return self.signed_data.encode("utf8")

    @property
    def signature_bytes(self) -> bytes:
        return Base64UrlEncoder.decode(self.signature)

    @pyd.model_serializer
    def ser_model(self) -> dict[str, t.Any]:
        """Custom model serializer to serialize fields with their alias names.

        Returns:
            dict[str, t.Any]: model serialzied as dict.
        """
        # https://github.com/pydantic/pydantic/issues/8379
        # for now, hard code the serializer
        return {
            "header": self.header,
            "payload": self.payload,
            "signedData": self.signed_data,
            "signature": self.signature,
        }

    @classmethod
    def decode(cls, encoded_ucan: str) -> te.Self:
        try:
            decoded_token = Base64UrlEncoder.unverified_decode_complete(encoded_ucan)

            raw_header = decoded_token["header"]
            token_header = UcanHeader.model_validate(raw_header, strict=False)

            raw_payload = decoded_token["payload"]
            token_payload = UcanPayload.model_validate(raw_payload, strict=False)

            signature_bytes = decoded_token["signature"]
            encoded_header, encoded_payload, encoded_signature = encoded_ucan.split(".")
            signed_data = f"{encoded_header}.{encoded_payload}"

            return cls(
                header=token_header,
                payload=token_payload,
                signed_data=signed_data,
                signature=Base64UrlEncoder.encode(signature_bytes),
            )

        except ValueError as err:
            msg = (
                f"Can't parse UCAN: {encoded_ucan}: Expected JWT format: "
                "3 dot-separated base64url-encoded values."
            )
            raise ValueError(msg) from err

    def encode(self) -> str:
        """Returns the JWT representation of UCAN.

        Returns:
            str: JWT representation of UCAN.
        """
        return f"{self.signed_data}.{self.signature}"
