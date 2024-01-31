from pprint import pprint
from utils import hash_function, padding

def prepare_plaintexts(plaintext, key):
    '''
        Prepares the plaintext by padding and hashing it.
    '''
    padded_plaintext = [padding(text, key) for text in plaintext]
    # print("preprocessing: Padded plaintext: ")
    # pprint(padded_plaintext)
    
    hashes = [hash_function(text) for text in padded_plaintext]
    # print("preprocessing: Hashes: ")
    # pprint(hashes)

    return padded_plaintext, hashes
