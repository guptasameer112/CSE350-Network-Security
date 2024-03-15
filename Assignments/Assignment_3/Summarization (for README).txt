-> Public Key CA: Responds to clients asking for their own RSA-based public key certificates or of others.
-> 2 clients: 
	1. Send request to CA for their own public-key certificates or of others.
	2. Exchange messages between client_1 and client_2, in confidentiality, after knowing the public key of the recipient in a secure manner (Obtain public key of recipient from CA).

-> Fields of the certificate:
CERTA = [(IDA, PUA, TA, DURA, IDCA) || ENCPR-CA (IDA, PUA, TA, DURA, IDCA)]
IDA: user ID of A
PUA: Public key of A
TA: Time of issuance of certificate
DURA: Duration of certificate validity
ENCPR-CA: Encryption through private key of certificate Authority

-> Assumption:
	- Clients know their public and private keys but not certificates.
	- Clients know the public key of the certificate authority.
	- CA has the public keys of all the clients.

-> Test:
	- Determine each other's public keys.
	- Client A sends 3 messages to B, and B responds with acknowledgements.

-> Methods:
	- Encrypt messages from CA to clients using RSA algorithm and CA's private key.
	- Once client's have each others public keys, they send encrypted messages.
	- Generate and Encode "current time" and "duration".

