from des import encrypt, decrypt

def main():
    hex_plaintext = "ABDC64397538AB00"
    hex_key = "133457799BBCDFF1"

    print("Plaintext (Hex)", hex_plaintext)
    print("Key (Hex)",hex_key)
    # Convert hexadecimal to binary
    binary_plaintext = bin(int(hex_plaintext, 16))[2:].zfill(64)
    binary_key = bin(int(hex_key, 16))[2:].zfill(64)

    print(f"Plaintext (Binary): {binary_plaintext}")
    print(f"Key (Binary): {binary_key}")

    # Encryption
    encrypted = encrypt(binary_plaintext, binary_key)
    print(f"Encrypted (Binary): {encrypted}")
    print(f"Encrypted (Hex): {hex(int(encrypted, 2))[2:].upper()}")

    # Decryption
    decrypted = decrypt(encrypted, binary_key)
    print(f"Decrypted (Binary): {decrypted}")
    print(f"Decrypted (Hex): {hex(int(decrypted, 2))[2:].upper()}")


if __name__ == "__main__":
    main()