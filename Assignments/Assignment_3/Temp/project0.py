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
        duration = timedelta(seconds=5)  # Valid for 5 seconds
        certificate_content = {
            'client_id': client_id,
            'client_public_key': client_public_key,
            'issuance_time': issuance_time.isoformat(),
            'duration': duration.total_seconds(),  # Store as total seconds
            'ca_id': self.ca_id,
        }

        certificate_hash = hash_data(json.dumps(certificate_content))
        certificate_signature = rsa_encrypt(certificate_hash, self.ca_private_key)
        self.certificates[client_id] = (certificate_content, certificate_signature)
        return certificate_content, certificate_signature
    
    def get_certificate(self, client_id):
        certificate = self.certificates.get(client_id, None)
        if certificate is None:
            raise ValueError("Certificate not found for client_id:", client_id)
        return certificate

# Client
class Client:
    def __init__(self, ca_public_key, ca):
        self.public_key, self.private_key = generate_rsa_keys()
        self.ca_public_key = ca_public_key
        self.ca = ca
        self.received_messages = []
        self.certificate = None
        self.certificate_signature = None

    def request_certificate(self):
        self.certificate, self.certificate_signature = self.ca.generate_certificate(id(self), self.public_key)

    def request_and_validate_certificate(self, other_client_id):
        try:
            other_certificate, other_signature = self.ca.get_certificate(other_client_id)
            if self.validate_certificate(other_certificate, other_signature):
                print(f"Successfully retrieved and validated certificate for client {other_client_id}")
                return other_certificate['client_public_key']
            else:
                print("Failed to validate the other client's certificate.")
                return None
        except ValueError as e:
            print(e)
            return None

    def send_message(self, recipient, message):
        encrypted_message = rsa_encrypt(message, recipient.public_key)
        recipient.receive_message(encrypted_message, self)

    def receive_message(self, encrypted_message, sender):
        decrypted_message = rsa_decrypt(encrypted_message, self.private_key)
        self.received_messages.append((id(sender), decrypted_message))
        print(f"Message from {id(sender)} to {id(self)}: {decrypted_message}")

    def validate_certificate(self, certificate, certificate_signature):
        certificate_hash = rsa_decrypt(certificate_signature, self.ca_public_key)
        expected_hash = hash_data(json.dumps(certificate))
        # Validate timestamp and duration
        issuance_time = datetime.fromisoformat(certificate['issuance_time'])
        duration = timedelta(seconds=certificate['duration'])  # Reconstruct timedelta from seconds
        if issuance_time + duration < datetime.now():
            return False  # The certificate has expired
        return certificate_hash == expected_hash

    def print_received_messages(self):
        print(f"Client {id(self)} has received the following messages:")
        for sender_id, message in self.received_messages:
            print(f"From {sender_id}: {message}")
            
def print_certificate(title, certificate):
    print(f"---------- {title} ----------")
    for key, value in certificate.items():
        print(f"{key}: {value}")
    print("--------------------------------------------------\n")



# Main execution: Setup CA, Clients, and Test Communication
def main():
    print("Initializing the Certificate Authority (CA)...")
    ca = CertificateAuthority()
    print(f"CA's public key: {ca.ca_public_key}")
    print("---------------------------------------------------------------\n")

    print("Creating Client A and Client B...")
    clientA = Client(ca.ca_public_key, ca)  # Pass CA's public key explicitly to the client
    clientB = Client(ca.ca_public_key, ca)
    print("Client A and Client B have been created.")
    print("--------------------------------------------------\n")

    print("Requesting Certificates for both clients from the CA...")
    clientA.request_certificate()
    clientB.request_certificate()
    print("Certificates obtained successfully.")
    print("--------------------------------------------------\n")

    # Request and validate certificates
    print("Client A attempts to retrieve and validate Client B's certificate...")
    clientA_public_key = clientA.request_and_validate_certificate(id(clientB))
    print("Client B attempts to retrieve and validate Client A's certificate...")
    clientB_public_key = clientB.request_and_validate_certificate(id(clientA))
    if not clientA_public_key or not clientB_public_key:
        print("Failed to exchange certificates. Exiting.")
        return
    
    print("--------------------------------------------------\n")

    # Using the function to print certificates
    print_certificate("Client A's Certificate", clientA.certificate)
    print_certificate("Client B's Certificate", clientB.certificate)

    print("Secure Message Exchange commencing...")
    print("Client A sends three messages to Client B...")
    clientA.send_message(clientB, "Hello from A to B - 1")
    clientA.send_message(clientB, "Hello from A to B - 2")
    clientA.send_message(clientB, "Hello from A to B - 3")
    print("Messages sent by Client A to Client B.")
    print("--------------------------------------------------\n")

    print("Client B acknowledges receipt by responding to Client A...")
    clientB.send_message(clientA, "ACK from B to A - 1")
    clientB.send_message(clientA, "ACK from B to A - 2")
    clientB.send_message(clientA, "ACK from B to A - 3")
    print("Acknowledgements sent by Client B to Client A.")
    print("--------------------------------------------------\n")

    # Showcasing message reception by printing the stored messages
    print("Reviewing messages exchanged...")
    clientA.print_received_messages()
    clientB.print_received_messages()
    
    print("Exploring Certificate Validation and Tampering...")
    print("Simulating an attempt to tamper with a certificate...")
    tampered_certificate, tampered_signature = ca.generate_certificate("Tampered", clientB.public_key)
    # Tampering with the certificate
    tampered_certificate['client_public_key'] = (999, 999)

    print("Attempting to validate the tampered certificate...")
    if not clientA.validate_certificate(tampered_certificate, tampered_signature):
        print("Validation failed: The certificate has been tampered with or is otherwise invalid.")
    else:
        print("Error: Tampered certificate unexpectedly passed validation. (This should not happen in a secure system.)")
    print("--------------------------------------------------\n")

    print("Demonstration concluded. System shut down.")

if __name__ == "__main__":
    main()



