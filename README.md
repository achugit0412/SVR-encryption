# SVR-encryption
🔐 Custom Multi-Layer Encryption System

📌 Overview

This project implements a custom multi-layer encryption system that combines both classical and modern cryptographic techniques.
It transforms a plaintext message into a highly obfuscated ciphertext through a series of independent steps, each adding an extra layer of security.

⚙️ How It Works

🔑 Key Generation

- A master key is generated using secure random bytes.
- A random nonce is created for each encryption.
- Three unique keys are derived using HMAC (SHA-256):
  - Key 1 → Vigenère cipher
  - Key 2 → Solitaire keystream
  - Key 3 → XOR mixing

🔄 Encryption Process

The encryption process consists of the following steps:

1. Vigenère Cipher

- Performs character substitution.
- Each letter is shifted based on key values.

2. Byte Conversion

- Converts the encrypted text into raw bytes.

3. Solitaire Keystream

- Generates a pseudo-random keystream using a deck-based algorithm.

4. XOR Mixing

- Combines:
  - Message bytes
  - HMAC-derived bytes
  - Solitaire keystream
- Provides strong data scrambling.

5. Rail Fence Cipher

- Rearranges characters in a zigzag pattern.
- Adds a transposition layer.

📦 Output Format

The final encrypted output is:

<nonce_hex>:<ciphertext>

- nonce_hex → Random value used for key derivation
- ciphertext → Fully encrypted message


🔓 Decryption Process

Decryption reverses all steps:

1. Extract nonce and regenerate keys
2. Undo Rail Fence cipher
3. Convert hex to bytes
4. Apply XOR mixing (reversible)
5. Apply Vigenère decryption

✔️ If the correct key is used, the original message is recovered exactly.

🚀 Usage

master_key = make_master_key()

message = "Hello! This is my secret message."

encrypted = encrypt(message, master_key)
print("Encrypted:", encrypted)

decrypted = decrypt(encrypted, master_key)
print("Decrypted:", decrypted)


✨ Features

- Multi-layer encryption approach
- Random nonce for unique outputs
- Combination of classical + modern cryptography
- Symmetric encryption system
- Fully reversible process


⚠️ Disclaimer

This project is intended for educational purposes only.

It is not a replacement for industry-standard encryption algorithms such as AES or RSA, and should not be used for securing sensitive or production data.


📚 Concepts Used

- HMAC (SHA-256)
- Vigenère Cipher
- Solitaire Cipher (Keystream generation)
- XOR Encryption
- Rail Fence Cipher
