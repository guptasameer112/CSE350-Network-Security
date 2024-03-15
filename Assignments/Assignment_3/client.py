import random
import json
from rsa import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from certificate_authority import CertificateAuthority, hash_data

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
