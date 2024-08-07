"""ucan.core.capability module."""

from __future__ import annotations

import typing as t
import typing_extensions as te

import pydantic as pyd
from pydantic_core import PydanticKnownError

from ucan.schemas import BaseModel, StringNonEmpty


__all__ = (
    "ResourcePointer",
    "Ability",
    "Capability",
)


class ResourcePointer(BaseModel):
    """Resource Pointer of a UCAN Capability representated as the `with` field."""

    SEPARATOR: t.ClassVar[str] = ":"

    scheme: StringNonEmpty
    hier_part: StringNonEmpty = pyd.Field(alias="hierPart")

    @pyd.model_serializer
    def ser_model(self) -> dict[str, t.Any]:
        """Custom model serializer to serialize fields with their alias names.

        Returns:
            dict[str, t.Any]: model serialzied as dict.
        """
        # https://github.com/pydantic/pydantic/issues/8379
        # for now, hard code the serializer
        return {"scheme": self.scheme, "hierPart": self.hier_part}

    @classmethod
    def decode(cls, data: str) -> te.Self:
        """Load ResourcePointer from string.

        `data` must be in the format: {scheme}{SEPARATOR}{hier_part}.

        Args:
            data (str): string representation of ResourcePointer.

        Raises:
            TypeError: Expected {separater} in the value.

        Returns:
            te.Self: ResourcePointer object.
        """
        if not isinstance(data, str):
            raise PydanticKnownError("string_type")

        parts = data.split(cls.SEPARATOR)
        if len(parts) < 2:  # noqa: PLR2004
            msg = f"Expected '{cls.SEPARATOR}' in the value"
            raise ValueError(msg)

        return cls(scheme=parts[0], hier_part=cls.SEPARATOR.join(parts[1:]))

    def __str__(self) -> str:
        """Returns a string representation of the ResourcePointer.

        The returned value is in the format: {scheme}{SEPARATOR}{hier_part}.

        Returns:
            str: String represenation of ResourcePointer.
        """
        return self.encode()

    def encode(self) -> str:
        """Returns a string representation of the ResourcePointer.

        The returned value is in the format: {scheme}{SEPARATOR}{hier_part}.

        Returns:
            str: String represenation of ResourcePointer.
        """
        return f"{self.scheme}{self.__class__.SEPARATOR}{self.hier_part}"


class Ability(BaseModel):
    """Ability of a UCAN Capability representated as the `can` field."""

    SEPARATOR: t.ClassVar[str] = "/"

    namespace: StringNonEmpty
    segments: list[StringNonEmpty]

    @classmethod
    def decode(cls, data: str) -> te.Self:
        """Load Ability from string.

        `data` must be in the format: {namespace}/segment1/segment2/etc.

        Args:
            data (str): string representation of Ability.

        Raises:
            TypeError: Expected {separater} in the value.

        Returns:
            te.Self: Ability object.
        """
        if not isinstance(data, str):
            raise PydanticKnownError("string_type")

        parts = data.split(cls.SEPARATOR)
        if len(parts) < 2:  # noqa: PLR2004
            msg = f"Expected '{cls.SEPARATOR}' in the value"
            raise ValueError(msg)

        return cls(namespace=parts[0], segments=parts[1:])

    def __str__(self) -> str:
        """Returns a string representation of the Ability.

        The returned value is in the format: namespace/segment1/segment2/etc

        Returns:
            str: String represenation of Ability.
        """
        return self.encode()

    def encode(self) -> str:
        """Returns a string representation of the Ability.

        The returned value is in the format: namespace/segment1/segment2/etc

        Returns:
            str: String represenation of Ability.
        """
        return self.__class__.SEPARATOR.join([self.namespace, *self.segments])


class Capability(BaseModel):
    """UCAN Capability represented in the list of `att` field."""

    with_: ResourcePointer = pyd.Field(alias="with")
    can: Ability

    @pyd.field_validator("with_", mode="before")
    def _validate_with(cls, data: str | t.Any) -> ResourcePointer | t.Any:  # noqa: ANN401
        """Optionally load the `with` field from string.

        Args:
            data (str | t.Any): field value.

        Returns:
            ResourcePointer | t.Any: ResourcePointer loaded from
                string or whatever the input was.
        """
        if isinstance(data, str):
            return ResourcePointer.decode(data)

        return data

    @pyd.field_validator("can", mode="before")
    def _validate_can(cls, data: str | t.Any) -> Ability | t.Any:  # noqa: ANN401
        """Optionally load the `can` field from string.

        Args:
            data (str | t.Any): field value.

        Returns:
            Ability | t.Any: Ability loaded from
                string or whatever the input was.
        """
        if isinstance(data, str):
            return Ability.decode(data)

        return data

    @pyd.model_serializer
    def ser_model(self) -> dict[str, t.Any]:
        """Custom model serializer to serialize fields with their alias names.

        Returns:
            dict[str, t.Any]: model serialzied as dict.
        """
        # https://github.com/pydantic/pydantic/issues/8379
        # for now, hard code the serializer
        return {"with": self.with_, "can": self.can}

    def encode(self) -> dict[str, str]:
        """Encode the individual parts of a capability.

        Returns:
            dict[str, str]: All fields with their encoded values.
        """
        return {"with": self.with_.encode(), "can": self.can.encode()}
