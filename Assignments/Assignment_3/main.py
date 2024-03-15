from certificate_authority import CertificateAuthority
from client import Client

def main():
    print("Initializing the Certificate Authority (CA)...")
    ca = CertificateAuthority()
    print("CA's public key:", ca.ca_public_key)
    print("---------------------------------------------------------------\n")

    print("Creating Client A and Client B...")
    clientA = Client(ca)
    clientB = Client(ca)
    print("--------------------------------------------------\n")

    print("Requesting Certificates...")
    clientA.request_certificate()
    clientB.request_certificate()

    # Using the new function to print certificates
    print("Client A's Certificate", clientA.certificate)
    print("Client B's Certificate", clientB.certificate)

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
