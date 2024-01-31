import time 
from pprint import pprint
from utils import verify_hash
from preprocessing import prepare_plaintexts
from encryption import encrypt
from decryption import decrypt
from bruteForce import brute_force

inputs = []
processed_plaintexts = []
hashes = []

ciphertexts = []
decrypted_plaintexts = []

# <-------------------------------------------------------------->

testfile = open('testfile.txt', 'r')
outputfile = open('outputfile.txt', 'w')

inputs = testfile.read().split('\n')
testfile.close()

outputfile.write("Inputs: \n")
outputfile.write(str(inputs))
outputfile.write("\n\n")

# <--------------------------Key 1----------------------------------> 

# Time benchmarking with K1
starttime = time.time()
key1 = "ihgfedcba" # Keys should have unique characters
processed_plaintexts, hashes = prepare_plaintexts(inputs, key1)
outputfile.write("Prepared plaintexts: \n")
outputfile.write(str(processed_plaintexts))
outputfile.write("\n\n")
# pprint(processed_plaintexts)
# pprint(hashes)

for plaintexts in processed_plaintexts:
    ciphertexts.append(encrypt(plaintexts, key1))
outputfile.write("Ciphertexts with hash: \n")
outputfile.write(str(ciphertexts))
outputfile.write("\n\n")
# pprint(ciphertexts)
    
encryptiontime = time.time() - starttime
print(f"Encryption time with K1: {encryptiontime}")

for ciphertext in ciphertexts:
    decrypted_plaintexts.append(decrypt(ciphertext, key1))
# pprint(decrypted_plaintexts)

outputfile.write("Decrypted plaintexts: \n")
outputfile.write(str(decrypted_plaintexts))
outputfile.write("\n\n")

for plaintext in range(len(decrypted_plaintexts)):
    for character in range(len(decrypted_plaintexts[plaintext])):
        if decrypted_plaintexts[plaintext][character] == "=":
            decrypted_plaintexts[plaintext] = decrypted_plaintexts[plaintext][:character]
            break

outputfile.write("Decrypted plaintexts without padding: \n")
outputfile.write(str(decrypted_plaintexts))
outputfile.write("\n\n")
    
decryptiontime = time.time() - starttime - encryptiontime
print(f"Decryption time with K1: {decryptiontime}")

# <-----------------------------Brute Forcing------------------------------>

# obtained_key, decrypted_plaintext = brute_force(ciphertexts[0])
# print("Brute force key:", obtained_key, "\n Decrypted plaintext:", decrypted_plaintext)

# brute_force_time = time.time() - starttime - encryptiontime - decryptiontime
# print(f"Brute force time: {brute_force_time}")


# <--------------------------END---------------------------------->

