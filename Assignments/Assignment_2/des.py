from permutations import permute
from utils import xor, IP, FP
from des_rounds import des_round
from key_generation import generate_keys

def des(input_bit_array, key_bit_array, encrypt=True):
    # Initial permutation
    permuted_input = permute(input_bit_array, IP)
    L, R = permuted_input[:32], permuted_input[32:]
    round_keys = generate_keys(key_bit_array)
    if not encrypt:
        round_keys.reverse()

    for round_num, round_key in enumerate(round_keys, start=1):
        # Modification to include round_num in des_round call
        L, R = R, xor(L, des_round(R, round_key, round_num))
        fprintf(f"{time.time()} - Round {round_num} - Output: {R}")

    # Final permutation
    pre_output = R + L  # Reverse R and L before final permutation
    return permute(pre_output, FP)

def encrypt(binary_plaintext, binary_key):
    return des(binary_plaintext, binary_key, True)

def decrypt(binary_ciphertext, binary_key):
    return des(binary_ciphertext, binary_key, False)
