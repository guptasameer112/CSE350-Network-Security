from permutations import permute
from utils import rotate_left, PC1, SHIFTS, PC2

def generate_keys(key_bit_array):
    # Key schedule
    key_permuted = permute(key_bit_array, PC1)
    L, R = key_permuted[:28], key_permuted[28:]
    round_keys = []
    for shift in SHIFTS:
        L, R = rotate_left(L, shift), rotate_left(R, shift)
        round_keys.append(permute(L + R, PC2))
    return round_keys
