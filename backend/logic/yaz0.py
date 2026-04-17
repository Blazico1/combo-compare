"""Pure-Python Yaz0 decompressor.

This implements the common Yaz0 decoding loop used by Nintendo SZS archives.
It only supports the standard Yaz0 variant used by Wii/GameCube files.

API:
    decompress(data: bytes) -> bytes

If `data` does not start with the Yaz0 magic, the input is returned as-is.
"""

from __future__ import annotations


def decompress(data: bytes) -> bytes:
    """Decompress a Yaz0-compressed bytes object.

    Raises ValueError on malformed input. If the input is not Yaz0, it is
    returned unchanged.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    if len(data) < 16 or data[0:4] != b"Yaz0":
        return bytes(data)

    # Uncompressed size is big-endian uint32 at offset 4
    uncompressed_size = int.from_bytes(data[4:8], "big")

    src = 16  # compressed data starts at offset 0x10
    src_len = len(data)
    dst = bytearray()

    # decode loop
    while len(dst) < uncompressed_size:
        if src >= src_len:
            raise ValueError("Unexpected end of input while reading code byte")
        code = data[src]
        src += 1

        for _ in range(8):
            # If MSB is set: literal
            if code & 0x80:
                if src >= src_len:
                    raise ValueError("Unexpected end of input while copying literal")
                dst.append(data[src])
                src += 1
            else:
                # Back-reference: read two bytes
                if src + 1 >= src_len:
                    raise ValueError("Unexpected end of input in backref")
                b1 = data[src]
                b2 = data[src + 1]
                src += 2

                # lower 12 bits = offset-1, upper 4 bits = length field
                dist = ((b1 & 0x0F) << 8) | b2
                dist += 1
                copy_len = (b1 >> 4) & 0x0F

                if copy_len == 0:
                    # extended length stored in next byte
                    if src >= src_len:
                        raise ValueError(
                            "Unexpected end of input reading extended length"
                        )
                    ext = data[src]
                    src += 1
                    copy_len = ext + 0x12
                else:
                    copy_len += 2

                # copy from previously decoded bytes
                if dist > len(dst):
                    raise ValueError("Back-reference distance exceeds decoded data")

                for _ in range(copy_len):
                    dst.append(dst[-dist])

            code = (code << 1) & 0xFF
            if len(dst) >= uncompressed_size:
                break

    # Truncate in case we over-copied (shouldn't normally happen)
    if len(dst) > uncompressed_size:
        return bytes(dst[:uncompressed_size])
    return bytes(dst)
