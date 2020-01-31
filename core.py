from Crypto.Cipher import AES
from scrypt import hash as schash
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from os.path import getsize
def keyderive(passphrase, salt):
	return schash(passphrase, salt, N=1048576, r=8, p=1, buflen=32)
	# ~30sec on laptop - N=104576, r=16, p=3

def encrypt(passphrase, plaintext):
	salt=get_random_bytes(256)
	key=keyderive(passphrase, salt)
	CipherEngine = AES.new(key, AES.MODE_GCM, nonce=get_random_bytes(12))
	ciphertext, mtag = CipherEngine.encrypt_and_digest(plaintext)
	return {'EncipheredData':ciphertext, 'MACTag':mtag, 'Nonce':CipherEngine.nonce, 'Salt':salt}

def decrypt(key, ciphertext, mtag, nonce):
	CipherEngine = AES.new(key, AES.MODE_GCM, nonce)
	return CipherEngine.decrypt_and_verify(ciphertext, mtag)

def encryptfile(inputpath, outputpath, passphrase, buflen=2048):
    salt=get_random_bytes(256)
    key=keyderive(passphrase,salt)
    CipherEngine = AES.new(key, AES.MODE_GCM, nonce=get_random_bytes(12))
    with open(inputpath, 'rb') as inf:
	    with open(outputpath, 'wb') as outf:
    		buf = inf.read(buflen)
    		while len(buf) > 0:
    			outf.write(CipherEngine.encrypt(buf))
    			buf=inf.read(buflen)
    		outf.write(CipherEngine.digest()) # MAC tag, 16 bytes
    		outf.write(CipherEngine.nonce) # nonce, 12 bytes
    		outf.write(salt) # salt, 256 bytes


def decryptfile(inputpath, outputpath, passphrase, readmode=0, buflen=2048):
	with open(inputpath, 'rb') as inf:
		fsize=getsize(inputpath)
		inf.seek(fsize-284)
		mac = inf.read(16)
		nonce = inf.read(12)
		salt = inf.read(256)
		inf.seek(0)
		cdatalength= fsize - 284
		pos=0
		CipherEngine = AES.new(keyderive(passphrase, salt), AES.MODE_GCM, nonce)
		with open(outputpath, 'wb') as outf:
			while pos < cdatalength:
				bytesleft=cdatalength-pos
				if bytesleft < buflen:
					outf.write(CipherEngine.decrypt(inf.read(bytesleft)))
					pos+=bytesleft
				else:	
					outf.write(CipherEngine.decrypt(inf.read(buflen)))
					pos+=buflen
			try:
				CipherEngine.verify(mac)
			except:
				raise ValueError('MAC Verification Failed! DO NOT trust data!')