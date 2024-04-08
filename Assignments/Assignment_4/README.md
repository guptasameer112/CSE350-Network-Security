
# CSE350: Network Security

## Programming Assignment 4: README


## Question

        On-the-go verification of Driver's License:

Verify the authenticity of a Driving License on the go.

Questions answered:

    1.  Information supplied by the driver and information obtained by the officer from the transport authority?
    A. 
    The driver provides their digital driver's license card, which contains information such as their name, address, date of birth, license number, license expiry date, and a digital photograph. 
    The police officer seeks and obtains the same information from the server in the transport authority, ensuring its authenticity and validity.

    2.  Is a central server required?
    A.
    Yes, a central server is needed to maintain correct and complete information on all drivers and the licenses issued to them.
    This central server acts as a trusted source of information, ensuring that only valid and authorized licenses are recognized.

    3.  Relevancy of Digital Signatures?
    A. 
    Digital signatures play a crucial role in ensuring the authenticity and integrity of the information exchanged between the driver's license card and the central server.
    Each digital driver's license card is signed by the transport authority using its private key, and the signature can be verified by the police officer using the transport authority's public key.

    4.  Does confidentiality of Information matter?
    A.
    Yes, it's essential to ensure both confidentiality and integrity during two-way communication between the driver's license card and the central server.
    Confidentiality ensures that sensitive information exchanged, such as the driver's personal details, is protected from unauthorized access.
    Integrity ensures that the information remains unchanged during transmission and cannot be tampered with by unauthorized parties.

    5.  Which of confidentiality, authenticity, Integrity and non-repudiation are relevant?
    A.
    Confidentiality: Relevant to protect the privacy of the driver's personal information.
    Authentication: Ensures that the driver's license information is authenticated by the transport authority before being accepted by the police officer.
    Integrity: Ensures that the information remains intact and unaltered during transmission between the driver's license card and the central server.
    Non-repudiation: Ensures that neither the driver nor the transport authority can deny the validity of the information exchanged.

    Bonus: Is date and time of communication important? How can it be obtained from the server in a secure manner?
    A. 
    Yes, the date and time of communication are essential for auditing and tracking purposes, especially when verifying the validity of a driver's license.
    Securely obtaining the date and time can be achieved by synchronizing with a trusted time server using secure protocols such as NTP (Network Time Protocol) over TLS (Transport Layer Security).




## Documentation

#### Main Menu Functionality:

**The main_menu() function**: presents a menu with options for registering a driver's license, checking a driver's license, printing all license data, printing the validity table, revoking a license, or exiting the program.


#### Registering a Driver's License:

**The register_license() function**: takes Aadhaar number, date of birth, and sex as input, encrypts them using the public key of the license authority, registers the license, signs the license data, and returns the encrypted license data along with its digital signature.


#### Checking a Driver's License:

**The check_license() function:** takes encrypted license data and its digital signature as input, decrypts the license data, verifies the signature using the public key of the license authority, and checks the validity of the license.


#### Utility Functions:

**print_all_licenses():** prints all registered licenses.
print_validity_table() prints the validity table containing hash values and their status.
revoke_license() revokes a license based on its ID.


#### Secure Communication:

**The secure_communicate() function:** encrypts and decrypts data using RSA encryption with OAEP padding and SHA-256 hashing for secure communication between the client and the license authority.


#### Additional Components:

**hash_license_data():** hashes the license data using SHA-256.
get_secure_ntp_time() securely obtains the current time from an NTP server, essential for timestamping and ensuring synchronization during operations.


## Demo

    1. Open the terminal and navigate to the directory where the code is present.
    2. Run the following command:
    
```bash
        python3 menu.py
```

## Sample Input and Outputs: 
**Input:** 

aadhaar=123456789101,dob=2027-02-02,sex=M,expiry_date=2025-04-08 21:22:49.181545

**Output:**
<img src = "public\Output.png">

## Authors

- [@Sameer Gupta](https://github.com/guptasameer112/CSE350-Network-Security/tree/main/Assignments/Assignment_4)
- [@Chaitanya Arora](https://github.com/guptasameer112/CSE350-Network-Security/tree/main/Assignments/Assignment_4)


