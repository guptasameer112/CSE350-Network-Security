import random
import hashlib
from sympy import isprime, mod_inverse
from datetime import datetime, timedelta
import json

# RSA Cryptography Functions
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

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Certificate Authority
class CertificateAuthority:
    def __init__(self, ca_id="CA1"):
        self.ca_public_key, self.ca_private_key = generate_rsa_keys()
        self.certificates = {}
        self.ca_id = ca_id

    def generate_certificate(self, client_id, client_public_key):
        issuance_time = datetime.now()
        duration = timedelta(days=365)  # Valid for 1 year
        certificate_content = {
            'client_id': client_id,
            'client_public_key': client_public_key,
            'issuance_time': issuance_time.isoformat(),
            'duration': str(duration),
            'ca_id': self.ca_id,
        }
        certificate_hash = hash_data(json.dumps(certificate_content))
        certificate_signature = rsa_encrypt(certificate_hash, self.ca_private_key)
        self.certificates[client_id] = (certificate_content, certificate_signature)
        return certificate_content, certificate_signature

# Client
class Client:
    def __init__(self, ca):
        self.public_key, self.private_key = generate_rsa_keys()
        self.ca = ca
        self.received_messages = []
        self.certificate = None
        self.certificate_signature = None

    def request_certificate(self):
        self.certificate, self.certificate_signature = self.ca.generate_certificate(id(self), self.public_key)

    def send_message(self, recipient, message):
        encrypted_message = rsa_encrypt(message, recipient.public_key)
        recipient.receive_message(encrypted_message, self)

    def receive_message(self, encrypted_message, sender):
        decrypted_message = rsa_decrypt(encrypted_message, self.private_key)
        print(f"Message from {id(sender)} to {id(self)}: {decrypted_message}")

    def validate_certificate(self, certificate, certificate_signature):
        # Simulating the process of decrypting the signature with the CA's public key
        certificate_hash = rsa_decrypt(certificate_signature, self.ca.ca_public_key)
        # Generating a hash of the received certificate content for comparison
        expected_hash = hash_data(json.dumps(certificate))
        # Comparing the decrypted signature (hash) with the expected hash
        return certificate_hash == expected_hash

def print_certificate(title, certificate):
    print(f"---------- {title} ----------")
    for key, value in certificate.items():
        print(f"{key}: {value}")
    print("--------------------------------------------------\n")

# Main execution: Setup CA, Clients, and Test Communication
def main():
    print("Initializing the Certificate Authority (CA)...")
    ca = CertificateAuthority()
    print("CA's public key:", ca.ca_public_key)
    print("---------------------------------------------------------------\n")

    print("Creating Client A and Client B...")
    clientA = Client(ca)  # Assuming CA object is correctly passed
    clientB = Client(ca)
    print("--------------------------------------------------\n")

    print("Requesting Certificates...")
    clientA.request_certificate()
    clientB.request_certificate()

    # Using the new function to print certificates
    print_certificate("Client A's Certificate", clientA.certificate)
    print_certificate("Client B's Certificate", clientB.certificate)

    print("Secure Message Exchange...")
    print("Client A sending messages to Client B...")
    clientA.send_message(clientB, "Hello1")
    clientA.send_message(clientB, "Hello2")
    clientA.send_message(clientB, "Hello3")

    print("\nClient B responding to Client A...")
    clientB.send_message(clientA, "ACK1")
    clientB.send_message(clientA, "ACK2")
    clientB.send_message(clientA, "ACK3")

    print("\nMessages received by Client B from Client A:", clientB.received_messages)
    print("Messages received by Client A from Client B:", clientA.received_messages)
    print("--------------------------------------------------\n")

    print("Simulating Certificate Tampering...")
    tampered_certificate, tampered_signature = ca.generate_certificate("Tampered", clientB.public_key)
    # Direct manipulation to simulate tampering
    tampered_certificate['client_public_key'] = (999, 999)

    print("Attempting to use tampered certificate...")
    if not clientA.validate_certificate(tampered_certificate, tampered_signature):
        print("Certificate validation failed. The certificate is tampered or invalid.")
    else:
        print("Tampered certificate unexpectedly passed validation.")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    main()
