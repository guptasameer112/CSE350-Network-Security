import itertools
from pprint import pprint
from decryption import decrypt

def generate_keys(min_length, max_length):
    '''
        Generates all possible keys with the given length range.
    '''

    keys = []
    available_characters = 'abcdefghi'

    for length in range(min_length, max_length + 1):
        for key in itertools.permutations(available_characters, length):
            keys.append(''.join(key))
    
    return keys

def brute_force(ciphertext_with_hash):
    '''
        Decrypts the ciphertext using brute force.
    '''
    for key in generate_keys(1, 9):
        decrypted_text, is_success = decrypt(ciphertext_with_hash, key)
        if is_success:
            print(f"Decrypted with key '{key}': {decrypted_text}")
            return key, decrypted_text
    
    print("No valid key found.")
    return None, None
