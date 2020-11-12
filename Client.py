import socket
import math 
import sympy
import math
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import hashlib
#############################################

class Client(object):
	"""docstring for Client"""
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect(('0.0.0.0', 8006))
		self.name = input("PLease Enter the NAME for RSA: ")  
		print("")

		self.l1=[character for character in self.name]  
		self.l2=[ord(character) for character in self.name]

		print(self.l1)
		print(self.l2)
		self.sums = sum(self.l2)
		print("")
		print("Sum of ASCII value is : " + str(self.sums))
		print("")
#####################################################
#AES
# This function is intended to provide the padding for the block size if the data left out doesnt fit the 16byte so padding is added, otherwise AES won't encrypt
	
	def pad(self, s):
		"""
			Arguments:
			--------------
			s: String 
				Short byte string to be padded to get 16 bytes of AES Block Size
		
			Description:
			--------------
			Function adds padding to short block to make it standard AES block of 16 bytes

		
			Returned Values:
			----------------
			Returns 16 bytes of padded block

		"""

		return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

# Encrypting the Message 
	def encrypt(self, message, key, key_size=256):
		"""
			Arguments:
			--------------
			message: bytes 
				message to be encrypted

			key: string
				AES key for encrypting message

			Key_size: int
				Size of the AES encryption key
		
			Description:
			--------------
			Function encrypts the message using AES CBC

		
			Returned Values:
			----------------
			Returns cipher text

		"""
		message = self.pad(message)
		# key = self.padKey(key)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(key, AES.MODE_CBC, iv)
		return iv + cipher.encrypt(message)

	def padBinKey(self,s):
		return r"0"*(128-len(str(s)) % 128) + str(s)

# Decrypting the Message
	def decrypt(self, ciphertext, key):
		"""
			Arguments:
			--------------
			ciphertext: bytes 
				ciphertext to be decrypted
		
			Description:
			--------------
			Function decrypts ciphertext of AES to plaintext

		
			Returned Values:
			----------------
			Returns plaintext msg
		"""
		iv = ciphertext[:AES.block_size]
		# key = self.padKey(key)
		cipher = AES.new(key, AES.MODE_CBC, iv)
		plaintext = cipher.decrypt(ciphertext[AES.block_size:])
		return plaintext.rstrip(b"\0")


# tackles the key generation using the SHA256 to be used for the AES encrytion
	def getAESHashKey(self,keyBin):
		"""
			Arguments:
			--------------
			KeyBin: bytes
				AES Starter key to get SHA256 Key
		
			Description:
			--------------
			Function calculates SHA256 key for AES

		
			Returned Values:
			----------------
			Returns the SHA256 Key

		"""
		hasher=SHA256.new(keyBin)
		self.key = bytes(hasher.digest())
		return self.key


	def rotateKey(self,key,n):
		"""
			Arguments:
			--------------
			key: int 
				key to be rotated for next round
			
			n:int
				number to which the AES 128-bit key is rotated 

			Description:
			--------------
			Function calculates primitive roots of prime number

		
			Returned Values:
			----------------
			Returns rotated key
		"""
		return key[n:] + key [:n]
#####################################################
# RSA

	def encryptRSA(self,rsaServerKey,key,n):
		"""
			Arguments:
			--------------
			rsaServerKey: int 
				public key of Server shared after RSA calcualtions

			Key: int
				value to be converted to hash

			n: int
				p * q, limit for rsa
		
			Description:
			--------------
			Function encrypts the key with provided rsaServerPublicKey and n. 

		
			Returned Values:
			----------------
			Returns encrypted hash
		"""

		encrypted = pow(key, rsaServerKey, n)
		return encrypted

	def decryptRSA(self,rsaClientPrivKey,hashed,n):	
		"""
			Arguments:
			--------------
			rsaClientPrivKey: int 
				Private key of Client shared after RSA calcualtions

			hasned: int
				value to be converted to key

			n: int
				p * q, limit for rsa
		
		
			Description:
			--------------
			Function decrypts the hash with provided rsaClientPrivKey and n. 

		
			Returned Values:
			----------------
			Returns decrypted key
		"""
		
		decrypted = pow(hashed,rsaClientPrivKey,n)
		print("Decrypted Value: {}".format(decrypted))
		return decrypted


	def getClientParameters(self):
		"""
			Description:
			--------------
			Function returns the parameters to initialized Client socket for further communication through this socket

		
			Returned Values:
			----------------
			returns Client socket obj
		"""
		return self.client

	def isPrime(self,num):
		"""
			Arguments:
			--------------
			num: int 
				Integer to be checked if prime

		
			Description:
			--------------
			Function returns True or False based on the number it prime or not.

		
			Returned Values:
			----------------
			Boolean values based on the Acceptance or Negation

		"""

		if num > 1: 
			for i in range(2, num,1):
				if ((num % i) == 0):
					return False

			return True

	def nextPrime(self,N): 
		"""
			Arguments:
			--------------
			N: int
				Number after which next prime is to be calculated

		
			Description:
			--------------
			Function calculates the next prime number after the number N described above.

		
			Returned Values:
			----------------
			Returns the next prime number

		"""
  
		if (N <= 1): 
			return 2
  
		prime = N 
		found = False
  
		while(not found): 
			prime = prime + 1
	
			if(self.isPrime(prime) == True): 
				found = True
  
		return prime


	def  calculateEncryptKey(self): 
		"""
	
			Description:
			--------------
			Function calculates Encryption key E, using the standard mechanism of p,q two prime numbers, ɸ & thus calculating E 

		
			Returned Values:
			----------------
			returns calculated E and Phi for decryption key calculation

		"""
		p = self.nextPrime(self.sums)
		q = self.nextPrime(p)

		print("The first prime number : p = "+ str(p))
		print("The second prime number : q = "+ str(q))
		print("")

		n = p * q
		fi = (p-1) * (q-1)

		print("Calculated n = " + str(n))
		print("Calculated fi(n) = " + str(fi)) 

		encKeysList=list()

		for i in range(2, fi,1): 
			if( math.gcd(i, fi) == 1 and self.isPrime(i) ):
				encKeysList.append(i)
				if len(encKeysList) >= 20:
					return (encKeysList,fi,n)

		return (encKeysList,fi,n)		

	def calculateDecryptKey(self,encKeysList, fi):
		"""
			Arguments:
			--------------
			encKeysList: int 
				Encryption keys list containing 20 keys for calculating inverse which is also a prime number
			fi: int
				Phi calculated by multiplication of decrementing p & q by 1

		
			Description:
			--------------
			Function calculates the Decryption key which is also prime

		
			Returned Values:
			----------------
			Returns the encryption key along with decryption key in the int format

		"""
		for encKey in encKeysList:
			for decKey in range(2, fi,1):
				if (((encKey*decKey) % fi) == 1):
					if (self.isPrime(decKey)):
						return (encKey,decKey)



def main():

	"""
		Description:
		--------------
		Execution point of program

	"""
	obj = Client()
	encKeysList,fi,nClient=obj.calculateEncryptKey()
	print("\nEncryption keys top 20 List : "+ str(encKeysList));
	encryption_key, decryption_key = obj.calculateDecryptKey(encKeysList, fi);
	print("Client RSA Enc key e : "+ str(encryption_key));
	print("CLIENT RSA Dec key (d) : " + str(decryption_key));

############################################

	client = obj.getClientParameters()
	server_rsa=str(client.recv(4096),"utf_8")
	server_rsa_key = int(server_rsa.split(":")[0])
	nServer = int(server_rsa.split(":")[1])
	print("\nServer RSA Enc KEY: {}".format(server_rsa_key))
	server_msg_rsa=str(encryption_key)+":"+str(nClient)
	client.send(bytes(server_msg_rsa,"utf_8"))

	from_server_diffie = client.recv(4096)
	server_msg=str(from_server_diffie,"utf_8")

	#server_rsa_key = int(server_msg.split(":")[0])
	diffie_q = obj.decryptRSA(decryption_key,int(server_msg.split(":")[0]),nClient) 
	diffie_a = obj.decryptRSA(decryption_key,int(server_msg.split(":")[1]),nClient)
	server_diffie_public_key=obj.decryptRSA(decryption_key,int(server_msg.split(":")[2]),nClient)



		
	print("SERVER DIFFIE PUBLIC KEY: {}".format(server_diffie_public_key))

	print("\nDIFFIE HELLMAN DANCE (CLIENT)!")
	print("Value of q is :" + str(diffie_q))
	print("Value of alpha a : " + str(diffie_a))

	private_key_Xa = int(input("\nEnter a private key whose value is less than q : "))
	public_key_Ya = pow(diffie_a, private_key_Xa , diffie_q)
	print("CLIENT DIFFIE Pulic key (Yb): "+ str(public_key_Ya))
	secret_key = pow(server_diffie_public_key, private_key_Xa, diffie_q) 

	print("FINAL SECRET: {}".format(secret_key))
	client_msg = str(public_key_Ya)
	client.send(bytes(client_msg,"utf_8"))


	AESkey = obj.padBinKey(bin(secret_key)[2:])
	print("\nAES KEY 128 Bit: {}\n".format(AESkey))

	AESKeyHash = obj.getAESHashKey(bytes(AESkey,"utf_8"))

	msgCount=1
	while True:

		try:
			

			server_chat = client.recv(4098)
			if server_chat:
				print("Server Chat Encrypted: {}".format(server_chat))
				print("Server Chat: {}\n".format(str(obj.decrypt(server_chat,AESKeyHash),"utf_8")))
				msgCount=msgCount+1
			

			if msgCount >= 7:
				server_data=''

				if server_data:
					server_data = client.recv(4096)
					testData=int(str(server_data,"utf_8"))
					testKey = obj.decryptRSA(decryption_key,testData,nClient) 
					AESkey = obj.padBinKey(bin(testKey)[2:])
					AESKeyHash=obj.getAESHashKey(bytes(AESkey,"utf_8"))
					print("\nKey Change: AES KEY 128 Bit: {}\n".format(AESkey))
					msgCount=1

				else:
					n=int(input("8th Message, enter times rotate n: "))
					testKey = obj.rotateKey(AESkey,n)
					intKey=int(testKey,2)
					rotatedKey = str(obj.encryptRSA(server_rsa_key,intKey,nServer))
					client.send(bytes(rotatedKey,"utf_8"))
					AESkey = testKey
					AESKeyHash=obj.getAESHashKey(bytes(AESkey,"utf_8"))
					print("\nKey Change: AES KEY 128 Bit: {}\n".format(AESkey))
					msgCount=1


			client_chat=input("Client > ")
			if client_chat:
				client_chat_enc=obj.encrypt(bytes(client_chat,"utf_8"),AESKeyHash)
				client.send(client_chat_enc)
				msgCount=msgCount+1
			
		except Exception as e:
			print(e)
		

	client.close()

##########################################


if __name__ == '__main__':
	main()
