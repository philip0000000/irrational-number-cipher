# irrational-number-cipher

This is a cipher that uses an irrational number as its key, commonly referred to as an "irrational cipher". The irrational number key is derived from the square root of a non-square number.

Written by philip0000000 <br>
Find the project here [https://github.com/philip0000000/OldFileFormatToXML] <br>
Program has been successfully tested on Windows 10 and Ubuntu 22.04 LTS with Python 3.10.

## Information

The author of this program is not a cryptography expert. It is not advised to rely on this program's encryption for real-world sensitive data, as it has not yet been thoroughly tested against cryptographic attacks. The author created this program to learn more about irrational numbers and encryption.

The idea of the program is to use the one-time pad[1], but with a key that is much shorter than the plaintext data that is going to be encrypted or vice versa (ciphertext to plaintext). One solution to this problem is to use stream ciphers[2]. However, this program uses an irrational number[3] to generate the key instead of a stream cipher.

The benefits of using an irrational number compared to a stream cipher for a key are:
1. A short stream cipher may repeat the key pattern, potentially compromising the security of the encryption. An irrational number as a key is endless and does not show a pattern.
2. Irrational numbers do not have intentional backdoors. Stream ciphers may contain intentional backdoors.

The drawback of using an irrational number compared to a stream cipher for a key is:
1. Encrypting with an irrational number should be slower than with stream cipher.

The program's cipher works with irrational numbers, which are obtained from the square roots of non-perfect square numbers. This yields an endless supply of irrational numbers[4]. The derived irrational number is then XOR-ed[5] with the plaintext, corresponding to the required numbers for each character. If the key is sufficiently random, using XOR logic should be sufficient to ensure good security[6].

## Usage

When selecting the number to generate a square root, it is recommended to use this specific command:
```
sqrtCipher.py -nsqrt
```
As this option generates the N-th non-square number, not using it may result in selecting a rational number if the square root is applied. An interesting algorithm was used to generate non-square numbers[7].

The length of the irrational number used for encryption must be three times greater than the length of the plaintext to be encrypted. This is because two decimal numbers are used to represent one character, and using three decimal numbers instead of two provides extra safety in case of any unexpected issues during encryption. To determine the size of a file, use the following command:
```
sqrtCipher.py -l
```

To generate the square root of a number with the desired number of digits, use the following command:
```
sqrtCipher.py -sqrt
```

To encrypt plaintext, use the command:
```
sqrtCipher.py -e
```

To decrypt the ciphertext, use the command:
```
sqrtCipher.py -de
```

To ensure that the encryption is secure against frequency analysis attacks, both the key and ciphertext must be sufficiently random. Two conditions must be correctly implemented to defend against such attacks:
1. Make sure that there is an equal frequency of all characters in the file. To verify this, use the following command:
```
sqrtCipher.py -di
```
2. Ensure that the characters are evenly distributed in the sequence, with sufficient spacing between them. Even though a sequence such as 0000011111 may pass the first test, it is not ideal. A better sequence would be 1010101010, as it exhibits a more random frequency distribution. To verify this in a file, use the following command:
```
sqrtCipher.py -dist
```

If the characters have the same "distribution of value" and "sum of value found distance", it means it is better.
<br><br>
If the key is not long enough for the plaintext, the key will wrap around during the encryption or decryption process. <br>
For checking encryption or decryption of non-text files such as PNG or JPG images, use the -b flag before any other command. The -b flag can only be used with -d, -di, -dd, and -dist commands.

#### Example:
1. Get length of file
```
python sqrtCipher.py -l long_plain_text.txt
36859   # 36859 * 3 = 110577 (length of square root number)
```
2. Get random non-square number
```
python sqrtCipher.py -nsqrt 83927923784947328923
83927923794108547389
```
3. Get the square root value
```
python sqrtCipher.py -sqrt 83927923794108547389 sqrt.txt 110577
```
4. Check that the square root value is the correct length
```
python sqrtCipher.py -l sqrt.txt
110578
```

5. Encrypt
```
python sqrtCipher.py -e long_plain_text.txt sqrt.txt long_plain_text2.txt
```
6. Decrypt
```
python sqrtCipher.py -de long_plain_text2.txt sqrt.txt long_plain_text3.txt
```

#### Check that the encryption is good
1. Check the character count in the encrypted file. Each character in the encrypted file should appear an equal number of times (1/255 = 0.003).
```
python sqrtCipher.py -di long_plain_text2.txt
```
2. Check the clustering of characters to ensure they are evenly distributed. All characters in the table should have the same value.
```
python sqrtCipher.py -dist long_plain_text2.txt
```

![square-root-irrational-number-cipher](example.jpg "example")

#### Schizophrenic number
Schizophrenic numbers[8] are numbers that show a specific pattern when their square roots are calculated. These numbers should be avoided. The formula to calculate schizophrenic numbers is:
```
f(n) = 10 f(n − 1) + n with the initial value f(0) = 0
```
One can also generate pseudo-schizophrenic numbers by repeating the digits "123456790". For example, consider the square root of 
123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790 is:
```
11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111.111111111111111111111111111111111111111111111111111111...
```
These numbers are not recommended to be used as a key when encrypting.

## License

Licensed under the MIT license.

## Reference

[1] https://en.wikipedia.org/wiki/One-time_pad <br>
[2] https://en.wikipedia.org/wiki/Stream_cipher <br>
[3] https://en.wikipedia.org/wiki/Irrational_number <br>
[4] https://www.quora.com/Are-all-non-perfect-square-numbers-square-roots-irrational-And-if-so-whats-the-proof-for-that <br>
[5] https://en.wikipedia.org/wiki/Exclusive_or <br>
[6] https://crypto.stackexchange.com/questions/47/with-sufficient-randomness-is-xor-an-acceptable-mechanism-for-encrypting <br>
[7] https://www.jstor.org/stable/3618253?seq=1 <br>
[8] https://en.wikipedia.org/wiki/Schizophrenic_number <br>
