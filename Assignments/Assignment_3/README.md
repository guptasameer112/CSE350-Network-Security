<h1> CSE350: Network Security </h1>
<h2><center> Programming Assignment 3: README </center></h2>

<!-- Question -->
## Question

<h2><u>Project: Public-Key Certificate Authority and Secure Communication</u></h2>

You are required to develop a program to implement a Public-Key Certificate Authority (CA) and two clients for secure communication. The CA responds to requests from clients seeking their own RSA-based public-key certificates or those of other clients. The clients can request their own certificates or those of others and exchange messages with each other in a confidential manner, encrypting them with the public key of the recipient after securely obtaining the recipient's public key.

<h3> a. Certificate Authority (CA):</h3>
<ul>
<li> The CA is responsible for generating RSA-based public-key certificates.
<li> It responds to requests from clients seeking their own certificates or those of other clients.
<li> The CA's functionalities include:
<ol>
<li> Generating RSA key pairs for clients.
<li> Generating and signing certificates containing client information, issuance time, duration, and CA ID.
<li> Maintaining a database of issued certificates.
Responding to certificate requests from clients.

> Fields in the certificate include:
> 
> **CERTA = [(IDA, PUA, TA, DURA, IDCA) || ENCPR-CA (IDA, PUA, TA, DURA, IDCA)]**
> <ul>
> <li> IDA: user ID of A
> <li> PUA: Public key of A
> <li> TA: Time of issuance of certificate
> <li> DURA: Duration of certificate validity
> <li> ENCPR-CA: Encryption through private key of certificate Authority
> </ul>

</ol>
</ul>

<h3> b. Clients:</h3>

<ul>
<li> Each client can request their own RSA-based public-key certificate from the CA or those of other clients.
<li> Clients exchange messages with each other in a confidential manner, encrypting them with the public key of the recipient after securely obtaining the recipient's public key.
<li> The clients' functionalities include:
<ol>
<li> Generating RSA key pairs.
<li> Requesting certificates from the CA.
<li> Exchanging messages with other clients securely using RSA encryption.
Verifying received certificates to ensure authenticity.
</ol>
</ul>

<h2> How to run the code: </h2>
1. Open the terminal and navigate to the directory where the code is present. <br>
2. Run the following command: <br>
   
```bash
    python3 main.py
```


<h2> Assumptions:</h2>
<ul>
<li> Clients know their public and private keys but not certificates.
<li> Clients know the public key of the certificate authority.
<li> The certificate authority has the public keys of all the clients.
</ul>

<h2> Test Cases:</h2>
<ul>
<li> Verify that clients can request their own public-key certificates from the CA.
<li> Verify that clients can request public-key certificates of other clients from the CA.
<li> Verify that the CA generates valid RSA-based certificates with correct information and signatures.
<li> Verify that clients can securely exchange messages with each other, encrypting them with the recipient's public key.
<li> Verify that messages decrypted using the recipient's private key yield the original plaintext.
</ul>

<h2> Methodology: </h2>

<h3> Certificate Authority (CA) Implementation: </h3>
<ul>
<li> The CertificateAuthority class is responsible for generating RSA key pairs, issuing certificates, and maintaining a database of issued certificates.
<li> Each CA instance initializes with its own RSA key pair and an empty certificate database.
<li> When a client requests a certificate, the CA generates a certificate containing client information, issuance time, and duration. It then signs the certificate using its private key and returns the certificate along with its signature.
</ul>

<h3> Client Implementation: </h3>
<ul>
<li> The Client class represents individual clients capable of requesting certificates from the CA, sending and receiving encrypted messages, and verifying received certificates.
<li> Each client instance generates its own RSA key pair upon initialization and stores its public and private keys.
<li> Clients request certificates from the CA by providing their public keys. Upon receiving a certificate, clients validate its authenticity by decrypting the signature using the CA's public key and comparing the computed hash with the expected hash of the certificate content.
<li> Clients can exchange messages securely by encrypting them with the recipient's public key and decrypting them using their private key.
</ul>

<h3> RSA Cryptography Functions: </h3>
<ul>
<li> The RSA encryption and decryption functions (rsa_encrypt and rsa_decrypt) are implemented using the standard RSA algorithm.
<li> Additional utility functions are provided for generating prime numbers (generate_prime), generating RSA key pairs (generate_rsa_keys), and hashing data (hash_data).
</ul>

<h2> Sample Input and Outputs: </h2>
<h3> Initial Certificate Authority (CA) and Client Setup: </h3>
<img src = "public\Initialisation.png">

<h3> Message Exchange between Clients: </h3>
<img src = "public\message_Exchange.png">

<h3> Certification Tampering Vertification: </h3>
<img src = "public\tampered_certificate_check.png">


<!-- END -->