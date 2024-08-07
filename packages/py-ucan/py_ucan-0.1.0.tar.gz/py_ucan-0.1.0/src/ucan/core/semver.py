"""ucan.core.semver module."""

from __future__ import annotations

import typing_extensions as te

from ucan.schemas import BaseModel


__all__ = ("SemVer",)


class SemVer(BaseModel):
    """UCAN version."""

    major: int
    minor: int
    patch: int

    @classmethod
    def decode(cls, value: str) -> te.Self:
        """Load `SemVer` from a string value.

        Args:
            value (str): String in the format major.minor.patch

        Returns:
            te.Self: `SemVer` object.
        """
        major, minor, patch = value.split(".")
        return cls.model_validate(
            {"major": major, "minor": minor, "patch": patch}, strict=False
        )

    def as_tuple(self) -> tuple[int, int, int]:
        """Encode `SemVer` as tuple.

        Returns:
            tuple[int, int, int]: `SemVer` as tuple in the format (major, minor, patch)
        """
        return self.major, self.minor, self.patch

    def encode(self) -> str:
        """Encode `SemVer` as string.

        Returns:
            str: `SemVer` as string in the format major.minor.patch
        """
        return f"{self.major}.{self.minor}.{self.patch}"

    def lt(self, other: SemVer) -> bool:
        """Check whether self version is less than other `SemVer`'s version.

        Args:
            other (SemVer): Other version to compare with.

        Returns:
            bool: Whether self is less than other.
        """
        return self.as_tuple() < other.as_tuple()
