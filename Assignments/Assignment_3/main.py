from certificate_authority import CertificateAuthority
from client import Client
from utils import print_certificate

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
    encrypted_text = clientA.send_message(clientB, "Hello from A to B - 1")
    print("Encrypted text:", encrypted_text)
    encrypted_text = clientA.send_message(clientB, "Hello from A to B - 2")
    print("Encrypted text:", encrypted_text)
    encrypted_text = clientA.send_message(clientB, "Hello from A to B - 3")
    print("Encrypted text:", encrypted_text)
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



