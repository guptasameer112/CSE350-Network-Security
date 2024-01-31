from utils import hash_function, key_mapping
from pprint import pprint

# <-------------------------------------------------------------->

def apply_transposition(text, key):
    '''
        Applies the transposition cipher to the plaintext.
    '''
    
    # print("Encryption: Applying transposition cipher, text: ", text, " key: ", key)

    ciphertext = ''
    matrix = []
    number_of_groups = len(text) // len(key)
    
    for i in range(number_of_groups):
        matrix.append(list(text[i * len(key): (i + 1) * len(key)]))

    # print("Encryption: Matrix: ")
    # pprint(matrix)

    for i in range(len(key)):
        for j in range(len(matrix)):
            ciphertext += matrix[j][key[i]]
    # print("Encryption: Ciphertext: ", ciphertext)

    return ciphertext

# <----------------------------------------------------------->

def encrypt(plaintext, key):
    '''
        Encrypts the plaintext using a transposition cipher and appends the hash in the form of a string
    '''

    # print("Encryption: Received plaintext: ", plaintext, " key: ", key)

    key1_indices = key_mapping(key)
    # print("Encryption: Key1 indices: ", key1_indices)

    ciphertext = apply_transposition(plaintext, key1_indices)
    # print("Encryption: Ciphertext: ", ciphertext)

    hash_of_plaintext = hash_function(plaintext)
    # print("Encryption: Hash of plaintext: ", hash_of_plaintext)

    ciphertext_with_hash = ciphertext + hash_of_plaintext
    # print("Encryption: Ciphertext with hash: ", ciphertext_with_hash)

    return ciphertext_with_hash