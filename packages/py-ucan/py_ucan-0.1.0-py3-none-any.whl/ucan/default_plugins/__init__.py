"""ucan.default_plugins package root."""

from .ed25519 import ed25519_plugin, EdKeypair


__all__ = (
    # ed25519 modules
    "ed25519",
    "ed25519_plugin",
    "EdKeypair",
)
