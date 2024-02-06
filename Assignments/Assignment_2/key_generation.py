from permutations import permute

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

def shift_left(k, shifts):
    """Shifts the given key k left by the number of shifts."""
    return k[shifts:] + k[:shifts]


def generate_subkeys(key):
    """Generates and returns 16 subkeys from the main key."""
    key = permute(key, PC1)  # Apply PC-1 to get 56-bit key
    L, R = key[:28], key[28:]
    subkeys = []
    for shift in SHIFTS:
        L = shift_left(L, shift)
        R = shift_left(R, shift)
        subkeys.append(permute(L + R, PC2))  # Apply PC-2 to get 48-bit key
    return subkeys

