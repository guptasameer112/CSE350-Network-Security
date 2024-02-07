<h1> CSE350: Network Security </h1>
<h2><center> Programming Assignment 2: README </center></h2>

<!-- Question -->
## Question
<b><u> Project 0: </u></b><br>
You are required to develop a program to encrypt (and similarly decrypt) a 64-bit plaintext using DES. Then, with at least THREE pairs of < plaintext, ciphertext>:

<b> a. </b> Verify that the ciphertext when decrypted will yield the original plaintext. <br>
<b> b. </b> Verify that output of the <u> 1st encryption round </u> is same as output of the  <u> 15th decryption round </u>. <br>
<b> c. </b> Verify that output of the<u> 14th encryption round </u> is same as the output of the <u> 2nd decryption round </u>.

<b><u> What is DES? </u></b><br>
The Data Encryption Standard (DES) is a symmetric-key block cipher algorithm widely used for encryption of electronic data. Developed in the early 1970s by IBM and adopted by the U.S. government as a federal standard in 1977, DES became one of the most widely used encryption algorithms worldwide. DES operates on 64-bit blocks of plaintext using a 56-bit key, making it a 56-bit block cipher.

<b><u> What does the DES algorithm include? </u></b><br>
The algorithm consists of:
<ul>
    <li> Key generation
    <li> Initial permutation
    <li> <b> 16 rounds of encryption (or decryption) </b>: During each round, DES employs permutation, substitution, and XOR operations to transform the plaintext into ciphertext.
    <li> Final permutation
</ul>

<b> Is it still in use? </b>:
DES is now considered insecure against modern cryptographic attacks due to its short key length. Consequently, it has been replaced by more secure algorithms like the Advanced Encryption Standard (AES).

<b><u> Encryption process: </u></b><br>
The encryption process is as follows: <br>
<ul>
<li> <b> Key Generation: </b> The 64-bit encryption key is transformed into 16 subkeys, each 48 bits long, using permutation and shifting operations.

<li> <b> Initial Permutation: </b> The 64-bit plaintext block is permuted according to the initial permutation table.

<li> <b> 16 Rounds of Encryption: </b> Each round consists of the following operations:

<ul>
<li> <b> Expansion: </b> The 32-bit half-block is expanded to 48 bits using the expansion permutation table.
<li> <b> Substitution: </b> The expanded half-block is divided into 6-bit segments, which are substituted using 8 S-boxes to produce a 32-bit output.
<li> <b> Permutation: </b> The output of the substitution step is permuted using the permutation table.
<li> <b> XOR with Subkey: </b> The permuted output is XORed with the corresponding 48-bit subkey.
</ul>
<li> <b> Final Permutation: </b> After the last round, the left and right halves of the block are swapped, and the final permutation is applied.
</ul>

<b><u> Decryption process: </u></b><br>
The decryption process is as follows: <br>
<ul>
<li> <b> Key Generation: </b> The same subkeys used in encryption are generated, but they are applied in reverse order.

<li> <b> Initial Permutation: </b> The 64-bit ciphertext block is permuted according to the initial permutation table.

<li> <b> 16 Rounds of Decryption: </b> Each round of decryption is similar to encryption, but the subkeys are applied in reverse order.

<li> <b> Final Permutation: </b> After the last round, the left and right halves of the block are swapped, and the final permutation is applied.
</ul>

<b><u> How to run the code: </u></b><br>
1. Open the terminal and navigate to the directory where the code is present. <br>
2. Edit the fields of ```ciphertext``` and ```key``` file to change the plaintext message and the key within the code. <br>
3. Run the following command: <br>
```python3 main.py``` <br>
1. The output will be displayed on the terminal <i> (integrity including original and obtained plaintexts and questions) </i> and in the outputfile.txt <i> (complete rounds) </i>. <br>

<b><u> Assumptions: </u></b>
-  Input and key is hexadecimal in nature.

<hr>
<div style="page-break-after: always;"></div>
<br><br>

<!-- Sample inputs and outputs -->
## Sample inputs and outputs
<br>
<b><u> Sample 1: </u></b><br>
<ul>
<li> <b> Input </b>: "123456789ABCDEF"
<li> <b> Output </b>: 

<img src = "public\output_1.png">
</ul>

<br><br>

<b><u> Sample 2: </u></b><br>
<ul>
<li> <b> Input </b>: "9929381AB"
<li> <b> Output </b>: 

<img src = "public\output_2.png">
</ul>

<br><br>

<b><u> Sample 3: Different Key </u></b><br>
<ul>
<li> <b> Input </b>: "8784BCD"
<li> <b> Output </b>: 

<img src = "public\output_3.png">
</ul>

