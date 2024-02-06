def xor(a, b):
    """XOR two strings of binary."""
    return ''.join('1' if i != j else '0' for i, j in zip(a, b))
