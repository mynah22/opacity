#! /usr/bin/python

from Crypto.Cipher import AES
from Crypto import Random
import Crypto.Hash.SHA256 as sha2
import time 
import os
class CipherEngine:
    '''Derives keys, encrypts and decrypts data.'''
    def __init__(self):
        self.hasher = sha2.new()
        self.keylist = []
        self.enlist = []
        self.delist = []
        self.hlist = []

    def keyderive(self, passphrase='', keyblocks=2, itr=222222):
        '''Input passphrase, key length, and hash iterations.
        Derives a key and stores it for use with 
        CipherEnginge.encrypt and CipherEngine.decrypt'''
        self.hasher = sha2.new()
        self.hasher.update(passphrase)
        if len(passphrase) < 16:
            offset = 16 - len(passphrase)
            keystub = passphrase +self.hasher.hexdigest()[0:offset]
        else:
            remainder = len(passphrase) % 16
            keystub = passphrase + self.hasher.hexdigest()[0:16-remainder]
        while len(keystub) < keyblocks * 16:
            self.hasher.update(keystub)
            keystub += self.hasher.hexdigest()
        while itr:
            self.hasher.update(keystub)
            keystub = self.hasher.hexdigest()
            itr -= 1
        self.fullk = keystub

    def _splitkeys(self):
        whole = self.fullk
        while whole:
            self.keylist.append(whole[0:16])
            whole = whole[16:]
    def setfile(self, target):
        '''Input filepath for reading of plaintext/ciphertext.'''
        self.fpath = target
        self.flength = os.path.getsize(target)
        self.fblocks = self.flength / 16
        if self.flength % 16:
            empty = 16 - (self.flength % 16)
            self.fblocks += 1

    def _xor(self, target, xr):
        position = 0
        target = bytearray(target)
        xr = bytearray(xr)
        while position < 16:
            target[position] ^= xr[position]
            position += 1
        return str(target)

    def _encryptcycle(self,plaintext, hashmode = False):
        self.keylist = []
        self._splitkeys()
        keysegs = list(self.keylist)
        textholder = str(plaintext)
        while keysegs:
            self.wrk = keysegs.pop(0)
            self.aes = AES.new(self.wrk)
            textholder = self.aes.encrypt(textholder)
        if hashmode:
            self.hlist.append(textholder)
        else:
            self.enlist.append(textholder)


    def _decryptcycle(self, ciphertext):
        self.keylist = []
        self._splitkeys()
        keysegs = list(self.keylist)
        textholder = str(ciphertext)
        while keysegs:
            self.wrk = keysegs.pop()
            self.aes = AES.new(self.wrk)
            textholder = self.aes.decrypt(textholder)
        return textholder

    def encrypt(self):
        '''Encrypts target by key. 
        CipherEngine.setfile and CipherEngine.keyderive must be used first.'''
        target = self.fpath
        completed = 0
        self.hasher = sha2.new()
       #create random initialization vector, hash iv for use as first exor
        iv = Random.new().read(16)
        self.hasher.update(iv)
        self.enlist.append(iv)
        xr = str(self.hasher.hexdigest())[-16:] 
       #read, encrypt, then exor file block by block, output to ciphertext list
        with open(target, 'rb') as f:
            while completed < self.fblocks:
                wrkblk = f.read(16)
                if len(wrkblk) < 16:
                    wrkblk += Random.new().read(16 - len(wrkblk))
                wrkblk = self._xor(wrkblk, xr)
                self._encryptcycle(wrkblk)
                xr = self.enlist[-1]
                completed+=1
       #hash ciphertext, encrypt it and add it to ciphertext list
        self.hasher = sha2.new()
        self.hasher.update(''.join(self.enlist))
        h = self.hasher.hexdigest()
        hblocks = 4
        completed = 0
        while completed < hblocks:
            hb = h[0:16]
            self._encryptcycle(hb, True)
            h = h[16:]
            completed += 1
        self.enlist.append(''.join(self.hlist))

    def decrypt(self):
        '''Decrypts target by key. 
        CipherEngine.setfile and CipherEngine.keyderive must be used first.'''
        target = self.fpath
        completed = 0
        targetlength = os.path.getsize(target)
        with open(target, 'rb') as f:
           #authenticate by decrypting last 4 blocks, and comparing
           #the result to the hash of the remaining chpertext
            self.hasher = sha2.new()
            hcompleted = 0
            hblocks = 4
            f.seek(targetlength - 64)
            h = ''
            while hcompleted < hblocks:
                cipherhashblock = f.read(16)
                plainhashblock = self._decryptcycle(cipherhashblock)
                self.hlist.append(plainhashblock)
                hcompleted += 1
            f.seek(0)
            authhash = ''.join(self.hlist)
            self.hasher = sha2.new()
            self.hasher.update(f.read(targetlength-64))
            truehash = self.hasher.hexdigest()
            if not truehash == authhash:
                raise Exception('Invalid passphrase, or file not encypted with\n'+
                                'this AES implementation.')
                exit()

           #if authenticated, then produce inital exor by hashing the random
           #text at the front of the file, and using the last block of the hash
           #as initial exor.
            f.seek(0)
            self.hasher = sha2.new()
            iv = f.read(16)
            self.hasher.update(iv)
            xr = str(self.hasher.hexdigest())[-16:]
           #read, exor, then decrypt file block by block, output to plaintext list
           
            while completed < self.fblocks -5:
                wrkblk = f.read(16)
                xrh = wrkblk 
                deciphertext = self._decryptcycle(wrkblk)
                plaintext = self._xor(deciphertext, xr)
                xr = xrh
                self.delist.append(plaintext)
                completed +=1

if __name__ == "__main__":
    import time,commands
