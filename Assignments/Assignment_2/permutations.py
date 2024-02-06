def permute(block, table):
    """General permutation function."""
    return ''.join(block[i - 1] for i in table)