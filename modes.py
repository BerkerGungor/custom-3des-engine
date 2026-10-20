"""
Block cipher modes of operation for 3DES: ECB and CBC modes.
"""

import os
from typing import Tuple
from des_core import triple_des_decrypt_block, triple_des_encrypt_block
from utils import pkcs7_pad, pkcs7_unpad


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    """Performs bitwise XOR between two byte sequences."""
    return bytes(x ^ y for x, y in zip(a, b))


def encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes = None) -> Tuple[bytes, bytes]:
    """
    Encrypts arbitrary-length data using 3DES in CBC mode.
    Returns (ciphertext, iv).
    """
    if len(key) != 24:
        raise ValueError("3DES key must be exactly 24 bytes.")

    if iv is None:
        iv = os.urandom(8)
    elif len(iv) != 8:
        raise ValueError("IV must be exactly 8 bytes.")

    padded_data = pkcs7_pad(plaintext, block_size=8)
    ciphertext = bytearray()
    prev_block = iv

    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i + 8]
        xored = _xor_bytes(block, prev_block)
        encrypted_block = triple_des_encrypt_block(xored, key)
        ciphertext.extend(encrypted_block)
        prev_block = encrypted_block

    return bytes(ciphertext), iv


def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Decrypts ciphertext using 3DES in CBC mode and strips PKCS#7 padding.
    """
    if len(key) != 24:
        raise ValueError("3DES key must be exactly 24 bytes.")
    if len(iv) != 8:
        raise ValueError("IV must be exactly 8 bytes.")
    if len(ciphertext) % 8 != 0 or len(ciphertext) == 0:
        raise ValueError("Ciphertext length must be a non-zero multiple of 8 bytes.")

    decrypted_padded = bytearray()
    prev_block = iv

    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i + 8]
        decrypted_block = triple_des_decrypt_block(block, key)
        plaintext_block = _xor_bytes(decrypted_block, prev_block)
        decrypted_padded.extend(plaintext_block)
        prev_block = block

    return pkcs7_unpad(bytes(decrypted_padded))


def encrypt_ecb(plaintext: bytes, key: bytes) -> bytes:
    """
    Encrypts arbitrary-length data using 3DES in ECB mode (independent blocks).
    """
    if len(key) != 24:
        raise ValueError("3DES key must be exactly 24 bytes.")

    padded_data = pkcs7_pad(plaintext, block_size=8)
    ciphertext = bytearray()

    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i + 8]
        ciphertext.extend(triple_des_encrypt_block(block, key))

    return bytes(ciphertext)


def decrypt_ecb(ciphertext: bytes, key: bytes) -> bytes:
    """
    Decrypts ciphertext using 3DES in ECB mode and strips PKCS#7 padding.
    """
    if len(key) != 24:
        raise ValueError("3DES key must be exactly 24 bytes.")
    if len(ciphertext) % 8 != 0 or len(ciphertext) == 0:
        raise ValueError("Ciphertext length must be a non-zero multiple of 8 bytes.")

    decrypted_padded = bytearray()

    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i + 8]
        decrypted_padded.extend(triple_des_decrypt_block(block, key))

    return pkcs7_unpad(bytes(decrypted_padded))