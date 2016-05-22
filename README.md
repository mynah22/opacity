# opacity
A python AES implementation


Opacity uses the Riejndahl cipher and the 256-bit Secure Hashing Algorithm via the Crypto package in the python standard library. There is currently a functioning command-line api, and I have a broken web gui. I will commit the webgui when it becomes more functional. 

See the usage.txt document for usage instructions.




Known issues:

  1) Shebang is possibly platform-dependant

  2) Decryption leaves padding


Areas of desired improvement:

  1) Better PBKD

  2) More practical file i/o 

  3) Web gui

  4) Documentation
  
  
  
  
  
  
Help for command line interface:

usage: cmd.py [-h] (-e | -d) [-p PASSPHRASE] [-i INPUTPATH] [-o OUTPUTPATH]
              [-r]

optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         Encrypts a file.
  -d, --decrypt         Decrypts a file.
  -p PASSPHRASE, --passphrase PASSPHRASE
                        ONLY FOR TESTING. passes passpharse on command line,
                        and therefore may be recorded.
  -i INPUTPATH, --inputpath INPUTPATH
                        path to input
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Path to output.
  -r, --read            Read file to stdout; do not save output. overrides -o

