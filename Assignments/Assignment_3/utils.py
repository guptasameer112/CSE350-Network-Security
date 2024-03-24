import hashlib

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

def print_certificate(title, certificate):
    print(f"---------- {title} ----------")
    for key, value in certificate.items():
        print(f"{key}: {value}")
    print("--------------------------------------------------\n")