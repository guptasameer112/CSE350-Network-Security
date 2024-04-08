import json
from datetime import timedelta, datetime
from ntp_client import get_secure_ntp_time
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

licenses_db = {}
validity_table = {}

def secure_communicate(data, key, operation="encrypt", is_signature=False):
    """
    Perform secure communication with encryption/decryption.

    Args:
        data (bytes or str): The data to be encrypted or decrypted.
        key (RSA private or public key): The key used for encryption or decryption.
        operation (str): The operation to perform - 'encrypt' or 'decrypt'.
        is_signature (bool): Indicates whether the data is a signature.

    Returns:
        bytes or str: Encrypted or decrypted data.
    """
    if operation == "encrypt":
        encrypted = key.encrypt(
            data.encode() if isinstance(data, str) else data,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
        print("Encrypted Data:", encrypted)
        return encrypted
    elif operation == "decrypt":
        decrypted = key.decrypt(
            data,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None)) 
        print("Decrypted Data:", decrypted)
        return decrypted.decode() if not is_signature else decrypted

def hash_license_data(license_data):
    """
    Hash the license data using SHA-256.

    Args:
        license_data (str): The license data to be hashed.

    Returns:
        bytes: The hash value.
    """
    digest = hashes.Hash(hashes.SHA256())
    digest.update(json.dumps(license_data).encode())
    return digest.finalize()

# def register_license(aadhaar, dob, sex):
#     """
#     Register a driver's license.

#     Args:
#         aadhaar (str): Aadhaar number of the license holder.
#         dob (str): Date of birth of the license holder (format: YYYY-MM-DD).
#         sex (str): Sex of the license holder (M/F/O).

#     Returns:
#         tuple: Encrypted license data and its signature.
#     """
#     # Check if Aadhaar number already exists in licenses_db
#     for data in licenses_db.values():
#         if f'aadhaar={aadhaar}' in data:
#             raise ValueError("A license with this Aadhaar number already exists.")

#     # Proceed with license registration
#     license_data = f'aadhaar={aadhaar},dob={dob},sex={sex},expiry_date={get_secure_ntp_time() + timedelta(days=365)}'  
#     license_hash = hash_license_data(license_data)
    
#     license_id = len(licenses_db) + 1
#     licenses_db[license_id] = license_data
#     validity_table[license_hash] = 'valid'
    
#     signature = private_key.sign(
#         license_hash,
#         rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH),
#         hashes.SHA256()
#     )
    
#     encrypted_license_data = secure_communicate(license_data, public_key)

#     # Logging to a text file
#     log_file_path = "license_registration_log.txt"
#     with open(log_file_path, "a") as log_file:
#         log_file.write(f"License ID: {license_id}\n")
#         log_file.write(f"Aadhaar: {aadhaar}\n")
#         log_file.write(f"Date of Birth: {dob}\n")
#         log_file.write(f"Sex: {sex}\n")
#         log_file.write(f"License Data: {license_data}\n")
#         log_file.write(f"Encrypted License Data: {encrypted_license_data}\n")
#         log_file.write(f"Digital Signature: {signature.hex()}\n")
#         log_file.write("\n")

#     return encrypted_license_data, signature



# def check_license(license_data, signature):
#     """
#     Check the validity of a driver's license.

#     Args:
#         license_data (str): The license data.
#         signature (bytes): The digital signature.

#     Returns:
#         str: Verification result message.
#     """
#     license_hash = hash_license_data(license_data)
    
#     try:
#         public_key.verify(
#             signature, 
#             license_hash,
#             rsa_padding.PSS(mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH),
#             hashes.SHA256()
#         )
#     except InvalidSignature:
#         return "Signature verification failed."

#     expiry_date_str = license_data.split(",")[-1].split("=")[-1]
#     try:
#         expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d %H:%M:%S.%f")
#         if get_secure_ntp_time() > expiry_date:
#             return "License has expired."
#     except ValueError:
#         return "Expiry date is missing or incorrect in the license data."
    
#     if license_hash not in validity_table:
#         return "License is not valid."
#     elif validity_table[license_hash] == 'valid':
#         return "Signature verified and license is valid."
#     else:
#         return "License has been revoked."


def register_license(encrypted_aadhaar, encrypted_dob, encrypted_sex):
    """
    Register a driver's license.

    Args:
        encrypted_aadhaar (bytes): Encrypted Aadhaar number of the license holder.
        encrypted_dob (bytes): Encrypted Date of birth of the license holder.
        encrypted_sex (bytes): Encrypted Sex of the license holder.

    Returns:
        tuple: Encrypted license data and its signature.
    """
    # Decrypt the encrypted data
    aadhaar = secure_communicate(encrypted_aadhaar, private_key, operation="decrypt")
    dob = secure_communicate(encrypted_dob, private_key, operation="decrypt")
    sex = secure_communicate(encrypted_sex, private_key, operation="decrypt")

    # Check if Aadhaar number already exists in licenses_db
    for data in licenses_db.values():
        if f'aadhaar={aadhaar}' in data:
            raise ValueError("A license with this Aadhaar number already exists.")

    # Proceed with license registration
    license_data = f'aadhaar={aadhaar},dob={dob},sex={sex},expiry_date={get_secure_ntp_time() + timedelta(days=365)}'  
    license_hash = hash_license_data(license_data)
    
    license_id = len(licenses_db) + 1
    licenses_db[license_id] = license_data
    validity_table[license_hash] = 'valid'
    
    signature = private_key.sign(
        license_hash,
        rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    
    encrypted_license_data = secure_communicate(license_data, public_key)

    # Logging to a text file
    log_file_path = "license_registration_log.txt"
    with open(log_file_path, "a") as log_file:
        log_file.write(f"License ID: {license_id}\n")
        log_file.write(f"Aadhaar: {aadhaar}\n")
        log_file.write(f"Date of Birth: {dob}\n")
        log_file.write(f"Sex: {sex}\n")
        log_file.write(f"License Data: {license_data}\n")
        log_file.write(f"Encrypted License Data: {encrypted_license_data}\n")
        log_file.write(f"Digital Signature: {signature.hex()}\n")
        log_file.write("\n")

    return encrypted_license_data, signature

def check_license(encrypted_license_data, signature):
    """
    Check the validity of a driver's license.

    Args:
        encrypted_license_data (bytes): Encrypted license data.
        signature (bytes): The digital signature.

    Returns:
        str: Verification result message.
    """
    # Decrypt the encrypted license data
    license_data = secure_communicate(encrypted_license_data, private_key, operation="decrypt")

    license_hash = hash_license_data(license_data)
    
    try:
        public_key.verify(
            signature, 
            license_hash,
            rsa_padding.PSS(mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
    except InvalidSignature:
        return "Signature verification failed."

    expiry_date_str = license_data.split(",")[-1].split("=")[-1]
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d %H:%M:%S.%f")
        if get_secure_ntp_time() > expiry_date:
            return "License has expired."
    except ValueError:
        return "Expiry date is missing or incorrect in the license data."
    
    if license_hash not in validity_table:
        return "License is not valid."
    elif validity_table[license_hash] == 'valid':
        return "Signature verified and license is valid."
    else:
        return "License has been revoked."

