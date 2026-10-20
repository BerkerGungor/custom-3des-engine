"""
CLI Demonstration for Custom 3DES Encryption Engine.
"""

from modes import decrypt_cbc, encrypt_cbc


def main():
    print("=" * 60)
    print("       CUSTOM 3DES (TRIPLE DES) ENCRYPTION ENGINE")
    print("=" * 60)

    # 24-byte (192-bit) 3DES master key
    key = b"MySecret3DESKey2026!#Pol"
    # Arbitrary length plaintext (not a multiple of 8 bytes)
    message = "Hello, this is a secret message encrypted by the custom 3DES engine!"

    print(f"\n[+] Original Plaintext : {message}")
    print(f"[+] Plaintext Length   : {len(message.encode('utf-8'))} bytes (non-block aligned)")
    print(f"[+] Master Key (ASCII) : {key.decode('latin-1')}")

    # CBC Mode Encryption
    plaintext_bytes = message.encode("utf-8")
    ciphertext, iv = encrypt_cbc(plaintext_bytes, key)

    print("\n" + "-" * 60)
    print("                 ENCRYPTION (CBC MODE)")
    print("-" * 60)
    print(f"[+] Initialization Vector (Hex) : {iv.hex()}")
    print(f"[+] Ciphertext (Hex)            : {ciphertext.hex()}")
    print(f"[+] Padded Output Length        : {len(ciphertext)} bytes")

    # CBC Mode Decryption
    decrypted_bytes = decrypt_cbc(ciphertext, key, iv)
    decrypted_message = decrypted_bytes.decode("utf-8")

    print("\n" + "-" * 60)
    print("                 DECRYPTION (CBC MODE)")
    print("-" * 60)
    print(f"[+] Decrypted Plaintext : {decrypted_message}")

    # Integrity verification
    assert message == decrypted_message, "Integrity check failed: Decrypted text does not match!"
    print("\n[✓] VERIFICATION SUCCESS: End-to-end data integrity confirmed.")
    print("=" * 60)


if __name__ == "__main__":
    main()