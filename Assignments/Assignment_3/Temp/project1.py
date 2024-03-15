import os
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
    
    def generate_nonce(length=16):
        return os.urandom(length).hex()

    def request_public_key(self, target_client_id):
        nonce = self.generate_nonce(16)
        encrypted_response = self.ca.request_public_key(id(self), target_client_id, nonce)
        if encrypted_response:
            response_decrypted = json.loads(rsa_decrypt(encrypted_response, self.ca.ca_public_key))
            if response_decrypted['nonce'] == nonce:
                print(f"Received and verified public key for {target_client_id}: {response_decrypted['public_key']}")
                return response_decrypted['public_key']
            else:
                print("Nonce mismatch. Possible replay attack.")
                return None
        else:
            print(f"Public key for {target_client_id} not found.")
            return None


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
        self.received_messages.append(decrypted_message)
        print(f"Message from {id(sender)} to {id(self)}: {decrypted_message}")

    def validate_certificate(self, certificate, certificate_signature):
        certificate_hash = rsa_decrypt(certificate_signature, self.ca.ca_public_key)
        expected_hash = hash_data(json.dumps(certificate))
        return certificate_hash == expected_hash
    
    def request_public_key(self, target_client_id):
        # Simulate requesting a public key for target_client_id from the PKDA
        print(f"Requesting public key for client {target_client_id} from PKDA...")
        if target_client_id in self.ca.certificates:
            target_public_key = self.ca.certificates[target_client_id][0]['client_public_key']
            print(f"Received public key for client {target_client_id}: {target_public_key}")
            return target_public_key
        else:
            print(f"No public key found for client {target_client_id}.")
            return None

def print_certificate(title, certificate):
    print(f"---------- {title} ----------")
    for key, value in certificate.items():
        print(f"{key}: {value}")
    print("--------------------------------------------------\n")
def main():
    # Initialize the Certificate Authority
    print("Initializing the Certificate Authority (CA)...")
    ca = CertificateAuthority()
    print("CA's public key:", ca.ca_public_key)
    print("---------------------------------------------------------------\n")

    # Create Client A and Client B
    print("Creating Client A and Client B...")
    clientA = Client(ca)
    clientB = Client(ca)
    print("Client A and Client B created and have their own keys.")
    print("--------------------------------------------------\n")

    # Clients request their certificates from the CA
    print("Requesting Certificates...")
    clientA.request_certificate()
    clientB.request_certificate()
    print("Certificates issued to Client A and Client B.")
    print("--------------------------------------------------\n")

    # Client A requests the public key of Client B from the PKDA
    print("Client A requesting the public key of Client B from the PKDA...")
    clientB_public_key = clientA.request_public_key(id(clientB))
    print(f"Client A received the public key of Client B: {clientB_public_key}")
    print("--------------------------------------------------\n")

    # Client B requests the public key of Client A from the PKDA
    print("Client B requesting the public key of Client A from the PKDA...")
    clientA_public_key = clientB.request_public_key(id(clientA))
    print(f"Client B received the public key of Client A: {clientA_public_key}")
    print("--------------------------------------------------\n")

    # Secure Message Exchange after obtaining each other's public keys
    print("Secure Message Exchange...")
    print("Client A sending encrypted messages to Client B...")
    messages_from_A_to_B = ["Hi1", "Hi2", "Hi3"]
    for msg in messages_from_A_to_B:
        clientA.send_message(clientB, msg)
    print("Client A sent messages to Client B.")
    print("--------------------------------------------------\n")

    print("Client B responding to Client A with encrypted messages...")
    responses_from_B_to_A = ["Got-it1", "Got-it2", "Got-it3"]
    for response in responses_from_B_to_A:
        clientB.send_message(clientA, response)
    print("Client B sent responses to Client A.")
    print("--------------------------------------------------\n")

    # Display messages received by Client B from Client A
    print("Messages received by Client B from Client A:")
    for msg in clientB.received_messages:
        print(msg)
    print("--------------------------------------------------\n")

    # Display messages received by Client A from Client B
    print("Messages received by Client A from Client B:")
    for response in clientA.received_messages:
        print(response)
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    main()
