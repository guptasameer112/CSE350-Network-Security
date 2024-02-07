from des import encrypt, decrypt

def main():
    hex_plaintext = "8784BCD"  # Example plaintext in hex
    hex_key = "CABF78"  # Example key in hex

    print("Plaintext (Hex)", hex_plaintext)
    print("Key (Hex)", hex_key)
    binary_plaintext = bin(int(hex_plaintext, 16))[2:].zfill(64)
    binary_key = bin(int(hex_key, 16))[2:].zfill(64)

    print(f"Plaintext (Binary): {binary_plaintext}")
    print(f"Key (Binary): {binary_key}")

    encrypted = encrypt(binary_plaintext, binary_key)
    print(f"Encrypted (Binary): {encrypted}")
    encrypted_hex = hex(int(encrypted, 2))[2:].upper()
    print(f"Encrypted (Hex): {encrypted_hex}")

    decrypted = decrypt(encrypted, binary_key)
    print(f"Decrypted (Binary): {decrypted}")
    decrypted_hex = hex(int(decrypted, 2))[2:].upper()
    print(f"Decrypted (Hex): {decrypted_hex}")


if __name__ == "__main__":
    main()