import hashlib
import json
from datetime import datetime, timedelta
from rsa import generate_rsa_keys, rsa_encrypt
from utils import hash_data

class CertificateAuthority:
    def __init__(self, ca_id="CA1"):
        self.ca_public_key, self.ca_private_key = generate_rsa_keys()
        self.certificates = {}
        self.ca_id = ca_id

    def generate_certificate(self, client_id, client_public_key):
        issuance_time = datetime.now()
        duration = timedelta(seconds=60)  # Valid for 60 seconds
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