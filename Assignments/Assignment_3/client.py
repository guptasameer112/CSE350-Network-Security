import random
import hashlib
import json
from datetime import datetime, timedelta
from rsa import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from certificate_authority import CertificateAuthority, hash_data

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
        return encrypted_message

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
