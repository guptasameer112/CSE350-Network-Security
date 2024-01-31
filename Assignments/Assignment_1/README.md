<h1> CSE350: Network Security </h1>
<h2><center> Programming Assignment 1: README </center></h2>

<!-- Question -->
## Question
<b><u> Project 2: </u></b><br>
Encryption & decryption using transposition of the kind discussed in class. Then develop the software to 
launch a brute-force attack to discover the key. Here assume that the key length is known to be 9 or less. <br>
<b> Character set is the 26 letters of the alphabet. </b>

<b><u> What algorithm are we using? </u></b><br>
We are using the single columnar transposition cipher. We had previously applied double transposition cipher, but the bruteforce capacity went too far. 

<b><u> Why are we using it? </u></b><br>
A single columnar transposition cipher offers several advantages, making it a useful encryption technique in certain scenarios:
<ul>
    <li> Ease of Implementation
    <li> Customizability
    <li> Resistance to Frequency Analysis
    <li> Suitability for Penetration Testing
</ul>

<b><u> Describing the key length limitations and complexity: </u></b><br>
According to the question, the key length is known to be 9 or less. So, we are using a smaller key lengths currently, so that our systems are able to test the brute force attack. <br>
The time complexity for the brute force attack is O(2^n), where n is the key length.

<b><u> Encryption process: </u></b><br>
The encryption process is as follows: <br>
1. The plaintext message is written into the first grid (first key) with needed padding, row by row, starting at the top left. <br>
2. The columns from step 1 are written into the second grid (second key) with needed padding. <br>
3. The ciphertext is often written out in blocks of 5.
4. Ciphertext + Hash (size = 64) is returned after encryption.

<b><u> Decryption process: </u></b><br>
The decryption process is as follows: <br>
To decrypt a double transposition, construct a block with the right number of rows under the keyword, blocking off the short columns. Write the cipher in by columns, and read it out by rows. Lather, rinse, repeat.

<b><u> Brute force attack: </u></b><br>
The brute force attack is as follows: <br>
1. The brute force attack is implemented using two functions that formulate all possible keys for the first and second transposition. <br>
2. For each key generated, the decryption process is applied. <br>
3. If the hash of the decrypted message matches the hash of the original message, the key is printed out. <br>

<b><u> How to run the code: </u></b><br>
1. Open the terminal and navigate to the directory where the code is present. <br>
2. Edit the "testfile.py" file to change the plaintext message and the key within the code. <br>
3. Run the following command: <br>
```python3 main.py``` <br>
4. The output will be displayed on the terminal (integrity) and in the outputfile.txt (complete lists). <br>

<b><u> Assumptions: </u></b>
- Two keys that are similar in length and key order, while being different, will be able to decrypt.
- 

<hr>
<div style="page-break-after: always;"></div>
<br><br>

<!-- Sample inputs and outputs -->
## Sample inputs and outputs
<br>
<b><u> Sample 1: </u></b><br>
<ul>
<li> <b> Input </b>: "The earth is like a ball with a big magnet in it."
<li> <b> Output </b>: 

<img src = "public\output_1.png">
<li> <b> Time </b>: 

<img src = "public\time_1.png">
</ul>

<br><br>

<b><u> Sample 2: </u></b><br>
<ul>
<li> <b> Input </b>: "If you want one piece of advice from me, it's to freeze your oranges before you eat them."
<li> <b> Output </b>: 

<img src = "public\output_2.png">
<li> <b> Time </b>: 

<img src = "public\time_2.png">
</ul>
