from Crypto.Cipher import AES
from scrypt import hash as schash
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import json
from Crypto.Util.Padding import unpad
def keyderive(passphrase, salt=0):
	if not salt:
		salt = get_random_bytes(256)
	return {'salt':salt, 'key':schash(passphrase, salt, N=1048576, r=8, p=1, buflen=32)}
	# ~30sec on laptop - N=104576, r=16, p=3

def encrypt(key, salt, plaintext):
	CipherEngine = AES.new(key, AES.MODE_GCM, nonce=get_random_bytes(12))
	ciphertext, mtag = CipherEngine.encrypt_and_digest(plaintext)
	return {'EncipheredData':ciphertext, 'MAC Tag':mtag, 'Nonce':CipherEngine.nonce, 'Salt':salt}

def decrypt(key, ciphertext, mtag, nonce):
	CipherEngine = AES.new(key, AES.MODE_GCM, nonce)
	return CipherEngine.decrypt_and_verify(ciphertext, mtag)

def encryptfile(inputpath, outputpath, key, salt=get_random_bytes(256)):
    with open(inputpath, 'rb') as inf:
    	edict=encrypt(key, salt, inf.read())
    	for k in edict:
    		edict[k] = b64encode(edict[k]).decode('utf-8')
    with open(outputpath, 'wb') as outf:
    	outf.write(json.dumps(edict).encode('utf-8'))

def decryptfile(inputpath, outputpath, passphrase, readmode=0):
	with open(inputpath, 'rb') as inf:
		ddict=json.loads(inf.read())
		for k in ddict:
			ddict[k] = b64decode(ddict[k])
		key=keyderive(passphrase, ddict['Salt'])['key']
		if readmode:
			return decrypt(key, ddict['EncipheredData'], ddict['MAC Tag'], ddict['Nonce'])
		else:
			with open(outputpath, 'wb') as outf:
				outf.write(decrypt(key, ddict['EncipheredData'], ddict['MAC Tag'], ddict['Nonce']))
