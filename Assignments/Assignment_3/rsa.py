import random
from sympy import isprime, mod_inverse

def generate_prime(n_bits=1024):
    while True:
        prime_candidate = random.getrandbits(n_bits)
        if isprime(prime_candidate):
            return prime_candidate

def generate_rsa_keys(n_bits=1024):
    p = generate_prime(n_bits)
    q = generate_prime(n_bits)
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def rsa_encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    encrypted_int = pow(message_int, e, n)
    return encrypted_int

def rsa_decrypt(encrypted_int, private_key):
    d, n = private_key
    decrypted_int = pow(encrypted_int, d, n)
    message_length = (decrypted_int.bit_length() + 7) // 8
    decrypted_message = decrypted_int.to_bytes(message_length, 'big').decode('utf-8')
    return decrypted_message
