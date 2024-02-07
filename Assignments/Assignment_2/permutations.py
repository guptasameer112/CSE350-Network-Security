def permute(input_bit_string, permutation_table):
    '''
        Generates permutations.
    '''
    return ''.join(input_bit_string[i - 1] for i in permutation_table)