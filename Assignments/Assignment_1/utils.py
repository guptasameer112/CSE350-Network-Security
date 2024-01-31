import hashlib
from pprint import pprint

# <----------------------------------------------------------->

def hash_function(plaintext):
    '''
        Input includes symbols.
        Computes a SHA-256 hash of the plaintext and then converts the hash into a string in the range 'a' to 'z'.
        The mapping is done as the universe presented is from 'a' to 'z'.
    '''

    # print("Utils Hashing: plaintext: ", plaintext)

    hash_hex = hashlib.sha256(plaintext.encode()).hexdigest()
    # print("Utils Hashing: hash: ", hash_hex)

    mapped_hash = ''.join(chr(ord('a') + int(char, 16) % 26) for char in hash_hex)
    # print("Utils Hashing: mapped hash: ", mapped_hash)

    return mapped_hash

# <----------------------------------------------------------->

def padding(plaintext, key):
    '''
        Adds padding to the plaintext based on the length of the key, in order to complete set lengths.
    '''

    # print("Utils Padding: plaintext: ", plaintext)

    if len(plaintext) % len(key) == 0:
        print("No need for padding.")
        return plaintext
    
    padded_plaintext = plaintext + '=' * (len(key) - len(plaintext) % len(key))
    # print("Padding required. Utils Padding: padded plaintext: ", padded_plaintext)

    return padded_plaintext

# <----------------------------------------------------------->

def key_mapping(key):
    """Converts a string key to permutation indices for the transposition cipher, handling repeating letters."""
    occurrence_dict = {}
    index_counter = 1
    permutation_indices = []
    
    for char in sorted(key):
        if char not in occurrence_dict:
            occurrence_dict[char] = 1
        else:
            occurrence_dict[char] += 1

        permutation_indices.append(index_counter)
        index_counter += 1
    
    char_to_indices = {char: [] for char in key}
    for index, char in enumerate(sorted(key)):
        char_to_indices[char].append(permutation_indices[index])
    
    final_indices = []
    for char in key:
        final_indices.append(char_to_indices[char].pop(0))
    for i in range(len(final_indices)):
        final_indices[i] = final_indices[i] - 1
    return final_indices


# <----------------------------------------------------------->

def verify_hash(plaintext, original_hash):
    computed_hash = hash_function(plaintext)
    if computed_hash == original_hash:
        print("Hashes match. Integrity verified.")
    else:
        print("Hashes do not match. Integrity compromised.")
