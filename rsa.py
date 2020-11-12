
import math
number = "umair" 	

def encryptRSA(rsaServerKey,key,n):
	# publickey = 19
	# n= 148987

	encrypted = pow(key, rsaServerKey, n)
	print(encrypted)
	return encrypted

def decryptRSA(rsaServerPrivKey,hashed,n):	
	# d= 101411
	decrypted = pow(hashed,rsaServerPrivKey,n)
	print(decrypted)
	return decrypted

enc=encryptRSA(19,856,148987)
dec=decryptRSA(101411,enc,148987)

print(enc)
print(dec)