import hashlib
from utils import hash_function, key_mapping, verify_hash
from pprint import pprint

# <---------------------------------------------------------------->

def apply_reverse_transposition(text, key):
    '''
        Applies the reverse transposition cipher to the ciphertext.
    '''

    # print("Decryption: Applying reverse transposition cipher, text: ", text, " key: ", key)
    
    decrypted_text = ''
    matrix = []
    num_rows = len(text) // len(key)
    index = 0

    matrix = [['' for _ in range(len(key))] for _ in range(num_rows)]
    # print("Decryption: Intialised Matrix: ")
    # pprint(matrix)
    
    for i in range(len(key)):
        for j in range(num_rows):
            matrix[j][key[i]] = text[index]
            index += 1
    # print("Decryption: Matrix: ")
    # pprint(matrix)

    decrypted_text = ''.join([''.join(row) for row in matrix])
    # print("Decryption: Decrypted text: ", decrypted_text)

    return decrypted_text

# <---------------------------------------------------------------->

def decrypt(ciphertext_with_hash, key):
    '''
        Decrypts the ciphertext and verifies the appended hash.
    '''

    # print("Decryption: ciphertext with hash: ", ciphertext_with_hash, " key: ", key)

    key_indices = key_mapping(key)
    # print("Decryption: key indices: ", key_indices)

    # Separating the ciphertext and the hash
    hash_length = 64

    ciphertext, appended_hash = ciphertext_with_hash[:-hash_length], ciphertext_with_hash[-hash_length:]
    # print("Decryption: ciphertext: ", ciphertext, " appended hash: ", appended_hash)

    decrypted_plaintext = apply_reverse_transposition(ciphertext, key_indices)
    # print("Decryption: plaintext: ", decrypted_plaintext)

    # Verifying the hash 
    verify_hash(decrypted_plaintext, appended_hash)

    return decrypted_plaintext
    