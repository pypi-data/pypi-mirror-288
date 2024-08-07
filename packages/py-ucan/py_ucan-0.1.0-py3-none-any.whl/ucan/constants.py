"""Constants."""
# https://github.com/ucan-wg/ts-ucan/blob/main/packages/default-plugins/src/prefixes.ts
# Each prefix is varint-encoded. So e.g. 0x1205 gets varint-encoded to 0x8524
# The varint encoding is described here: https://github.com/multiformats/unsigned-varint
# These varints are encoded big-endian in 7-bit pieces.
# So 0x1205 is split up into 0x12 and 0x05
# Because there's another byte to be read, the MSB of 0x05 is set: 0x85
# The next 7 bits encode as 0x24 (instead of 0x12) => 0x8524

# https://github.com/multiformats/multicodec/blob/e9ecf587558964715054a0afcc01f7ace220952c/table.csv#L94
PREFIX_DID_ALG_ED25519 = [b"\xed", b"\x01"]

PREFIX_DID_BASE58 = "did:key:z"  # z is the multibase prefix for base58btc byte encoding
