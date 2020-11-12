import socket
import math 
import sympy
import math
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import hashlib
########################################

class Server(object):
	"""docstring for Server"""
	def __init__(self):
		self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serv.bind(('0.0.0.0', 8006))
		self.serv.listen(5)
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
# Diffie Logic


	def gcd(self,a,b):
		while b != 0:
		   a, b = b, a % b
		return a

	def primRoots(self,modulo):
		"""
			Arguments:
			--------------
			modulo: int 
				Number whose primitive roots are to be calculated
		
			Description:
			--------------
			Function calculates primitive roots of prime number

		
			Returned Values:
			----------------
			Returns the list of primitive roots

		"""
		
		roots = []
		required_set = set(num for num in range (1, modulo) if self.gcd(num, modulo) == 1)

		for g in range(1, modulo):
			actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
			if required_set == actual_set:
			 roots.append(g)           
		return roots

	def encryptRSA(self,rsaClientKey,key,n):
		"""
			Arguments:
			--------------
			rsaClientKey: int 
				public key of client shared after RSA calcualtions

			Key: int
				value to be converted to hash

			n: int
				p * q, limit for rsa
		
			Description:
			--------------
			Function encrypts the key with provided rsaClientPublicKey and n. 

		
			Returned Values:
			----------------
			Returns encrypted hash
		"""

		encrypted = pow(key, rsaClientKey, n)
		print("Encrypted Value: {}".format(encrypted))
		return encrypted

	def decryptRSA(self,rsaServerPrivKey,hashed,n):	
		"""
			Arguments:
			--------------
			rsaServerPrivKey: int 
				Private key of Server shared after RSA calcualtions

			hasned: int
				value to be converted to key

			n: int
				p * q, limit for rsa
		
		
			Description:
			--------------
			Function decrypts the hash with provided rsaServerPrivKey and n. 

		
			Returned Values:
			----------------
			Returns decrypted key
		"""

		decrypted = pow(hashed,rsaServerPrivKey,n)
		print("Decrypted: {}".format(decrypted))
		return decrypted


####################################################

	def getServerParameters(self):
		"""
			Description:
			--------------
			Function returns the parameters to initialized Server socket for further communication through this socket

		
			Returned Values:
			----------------
			returns server socket obj
		"""
		return self.serv

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

		print("\nCalculated n = " + str(n))
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
		Execution point of program, This contains the main Flow of program and control segments

	"""
############################################
	obj = Server()
	encKeysList,fi,nServer=obj.calculateEncryptKey()
	print("\nEncryption keys top 20 List : "+ str(encKeysList));
	encryption_key, decryption_key = obj.calculateDecryptKey(encKeysList, fi);
	print("Server RSA Enc key e : "+ str(encryption_key));
	print("SERVER RSA Dec key (d) : " + str(decryption_key));


	serv = obj.getServerParameters()

############################################
# Diffie
	diffie_q = sympy.randprime(500,1000)
	print("\nDIFFIE HELLMAN DANCE (SERVER)!")
	print("Value of q is :" + str(diffie_q))

	primitive_roots = obj.primRoots(diffie_q)
	diffie_a=primitive_roots[-1]

	print("Value of alpha a : " + str(diffie_a))

	
	private_key_Xa = int(input("\nEnter a private key whose value is less than q : "))
	public_key_Ya = pow(diffie_a, private_key_Xa , diffie_q)
	print("SERVER DIFFIE PUBLIC KEY (Ya): "+ str(public_key_Ya))


#########################################

	while True:
		conn, addr = serv.accept()
		from_client = ''
	
		server_msg_rsa=str(encryption_key)+":"+str(nServer)
		conn.send(bytes(server_msg_rsa,"utf_8"))
		client_rsa=str(conn.recv(4098),"utf_8")
		client_rsa_key=int(client_rsa.split(":")[0])
		nClient=int(client_rsa.split(":")[1])
		print("\nClient RSA Enc KEY: {}".format(client_rsa_key))

		diffie_q_enc=obj.encryptRSA(client_rsa_key,diffie_q,nClient)
		diffie_a_enc=obj.encryptRSA(client_rsa_key,diffie_a,nClient)
		public_key_Ya_enc=obj.encryptRSA(client_rsa_key,public_key_Ya,nClient)
		server_msg_diffie=str(diffie_q_enc)+":"+str(diffie_a_enc)+":"+str(public_key_Ya_enc)

		conn.send(bytes(server_msg_diffie,"utf_8"))
		data = conn.recv(4096)
		from_client = str(data,"utf_8")
		#client_rsa_key=int(from_client.split(":")[0])

		client_diffie_public_key=int(from_client)
		print("Client DIFFIE PUBLIC KEY: {}".format(client_diffie_public_key))

		secret_key = pow(client_diffie_public_key, private_key_Xa, diffie_q) 
		print("FINAL SECRET: {}".format(secret_key))

		

		AESkey = obj.padBinKey(bin(secret_key)[2:])
		print("\nAES KEY 128 Bit: {}\n".format(AESkey))

		AESKeyHash = obj.getAESHashKey(bytes(AESkey,"utf_8"))
		
		msgCount=1
		while True:
			try:
				server_chat=input("Server > ")
				if server_chat:
					server_chat_enc=obj.encrypt(bytes(server_chat,"utf_8"),AESKeyHash)
					conn.send(server_chat_enc)
					msgCount=msgCount+1
					server_chat=''

				if msgCount >= 7:
					client_data = conn.recv(4096)
					if client_data:
						testData=int(str(client_data,"utf_8"))
						testKey = obj.decryptRSA(decryption_key,testData,nServer) 
						AESkey = obj.padBinKey(bin(testKey)[2:])
						AESKeyHash=obj.getAESHashKey(bytes(AESkey,"utf_8"))
						print("\nKey Change: AES KEY 128 Bit: {}\n".format(AESkey))
						msgCount=1

					else:
						n=int(input("8th Message, enter times rotate n: "))
						testKey = int(obj.rotateKey(AESkey,n))
						rotatedKey = str(obj.encryptRSA(client_rsa_key,testKey,nClient))
						conn.send(bytes(rotatedKey,"utf_8"))
						AESkey = obj.padBinKey(testKey)
						AESKeyHash=obj.getAESHashKey(bytes(AESkey,"utf_8"))
						print("\nKey Change: AES KEY 128 Bit: {}\n".format(AESkey))
						msgCount=1

				client_chat=conn.recv(4096)

				if client_chat:
					print("Client Chat Encrypted: {}".format(client_chat))
					print("Client Chat: {}\n".format(str(obj.decrypt(client_chat,AESKeyHash),"utf_8")))
					msgCount=msgCount+1.
					client_chat=''

			except:
				print('client disconnected')
				break
			
		conn.close()	

if __name__ == '__main__':
	main()
