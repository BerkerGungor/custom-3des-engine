# Custom 3DES Cryptography Engine

A modular Python implementation of the Triple Data Encryption Standard (3DES) running in Electronic Codebook (ECB) mode. This project demonstrates applied cryptography principles by implementing the core DES components from scratch, avoiding reliance on high-level security libraries.

## Architecture
This tool applies the standard DES algorithm three consecutive times per block, utilizing the encrypt-decrypt-encrypt sequence with independent keys to drastically enhance the security margin against brute-force attacks compared to standard DES.

## Features
- Complete manual implementation of standard DES S-Boxes, Permutations (IP, FP, E, P), and Key Scheduling (PC1, PC2).
- Bit-level XOR, left-shift, and binary manipulation functions.
- ECB mode operation for 64-bit independent block processing.
- Dynamic key generation from user input (8-character strings converted to 16-character hex keys).
- Secure hex-to-Latin1 and padding mechanisms for arbitrary message lengths.