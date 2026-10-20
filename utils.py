"""
Utility helpers for 3DES engine: data representation, hex/binary conversions,
and bitwise operations.
"""

from typing import List


# Helper functions for data conversion
def hex_to_bin(hex_string: str) -> str:
    """Converts a hexadecimal string to a binary string representation."""
    binary = ""
    for char in hex_string:
        binary += bin(int(char, 16))[2:].zfill(4)
    return binary


def bin_to_hex(binary: str) -> str:
    """Converts a binary string representation to a hexadecimal string."""
    hex_string = ""
    for i in range(0, len(binary), 4):
        hex_string += hex(int(binary[i:i + 4], 2))[2:]
    return hex_string


def string_to_hex(text: str) -> str:
    """Converts plain text characters to a hexadecimal string."""
    return ''.join([hex(ord(c))[2:].zfill(2) for c in text])


def hex_to_string(hex_string: str) -> str:
    """Converts a hexadecimal string back to ASCII text characters."""
    return ''.join([chr(int(hex_string[i:i + 2], 16)) for i in range(0, len(hex_string), 2)])


def pad_text(text: str) -> str:
    """Pad the text to make its length a multiple of 16 (for hex representation)."""
    padding_len = 16 - (len(text) % 16)
    if padding_len == 16:
        return text
    return text + "0" * padding_len


def str_to_hex_key(key_str: str) -> str:
    """Convert an 8-character key to a 16-character hex key."""
    key_str = key_str[:8].ljust(8, '!')
    hex_key = string_to_hex(key_str)
    return hex_key


def hex_to_latin1(hex_string: str) -> str:
    """Convert a hex string to Latin-1 (ISO 8859-1) encoded text."""
    byte_array = bytearray()
    for i in range(0, len(hex_string), 2):
        if i + 1 < len(hex_string):
            byte_value = int(hex_string[i:i + 2], 16)
            byte_array.append(byte_value)
    try:
        return byte_array.decode('latin-1')
    except UnicodeDecodeError:
        return "".join(chr(b) if b < 256 else '?' for b in byte_array)


# --- Bitwise Helpers for DES Core ---

def bytes_to_bits(data: bytes) -> List[int]:
    """Converts a bytes object into a list of individual bits (0s and 1s)."""
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def bits_to_bytes(bits: List[int]) -> bytes:
    """Converts a list of bits (multiple of 8) back into a bytes object."""
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte_val = 0
        for bit in bits[i:i + 8]:
            byte_val = (byte_val << 1) | bit
        out.append(byte_val)
    return bytes(out)


def xor_bits(a: List[int], b: List[int]) -> List[int]:
    """Performs bitwise XOR between two equal-length lists of bits."""
    return [x ^ y for x, y in zip(a, b)]


def pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
    """Pads data to a multiple of block_size using PKCS#7 standard."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data: bytes) -> bytes:
    """Validates and strips PKCS#7 padding from decrypted data."""
    if not data:
        raise ValueError("Cannot unpad empty data.")
    pad_len = data[-1]
    if pad_len == 0 or pad_len > 8:
        raise ValueError("Invalid PKCS#7 padding value.")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Corrupted PKCS#7 padding bytes.")
    return data[:-pad_len]


def pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
    """Pads data to a multiple of block_size using PKCS#7 standard."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data: bytes) -> bytes:
    """Validates and strips PKCS#7 padding from decrypted data."""
    if not data:
        raise ValueError("Cannot unpad empty data.")
    pad_len = data[-1]
    if pad_len == 0 or pad_len > 8:
        raise ValueError("Invalid PKCS#7 padding value.")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Corrupted PKCS#7 padding bytes.")
    return data[:-pad_len]