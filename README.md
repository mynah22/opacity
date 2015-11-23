# opacity
A python AES implementation


Opacity uses the Riejndahl cipher and the 256-bit Secure Hashing Algorithm via the Crypto package in the python standard library. There is currently a functioning command-line api, and I have a broken web gui. I will commit the webgui when it becomes more functional. 

Known issues:

1) Shebang is platform-dependant

2) Decryption leaves padding

3) Opens any size file (will read a 20gb file to ram)


Areas of desired improvement:
1) Better PBKD

2) More practical file i/o 

3) Web gui

4) Documentation
