import time
from utils import xor, SBOX, P, E
from permutations import permute

def s_box_substitution(input_bit_string):
    output = ""
    for i in range(8):  # For each S-box
        block = input_bit_string[i*6:(i+1)*6]
        row = int(block[0] + block[5], 2)
        column = int(block[1:5], 2)
        output += format(SBOX[i][row][column], '04b')
    return output

def des_round(input_half, key, round_num):
    """Performs one DES round with detailed printouts including timestamp."""
    expanded_half = permute(input_half, E)
    xor_result = xor(expanded_half, key)
    substituted = s_box_substitution(xor_result)
    permuted = permute(substituted, P)

    with open('output.txt', 'a') as f:
        f.write(f"{time.time()} - Round {round_num} - Input: {input_half}\n")
        f.write(f"{time.time()} - Round {round_num} - Key: {key}\n")
        f.write(f"{time.time()} - Round {round_num} - Expanded: {expanded_half}\n")
        f.write(f"{time.time()} - Round {round_num} - XOR: {xor_result}\n")
        f.write(f"{time.time()} - Round {round_num} - Substituted: {substituted}\n")
        f.write(f"{time.time()} - Round {round_num} - Permuted: {permuted}\n\n")

    return permuted