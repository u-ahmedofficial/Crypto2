import math 

name = input("PLease Enter the Name: ")  
print("")

l1=[character for character in name]  
l2=[ord(character) for character in name]

print(l1)
print(l2)
sums = sum(l2)
print("")
print("Sum of ASCII value is : " + str(sums))
print("")



def isPrime(num):
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

def nextPrime(N): 
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
	
		if(isPrime(prime) == True): 
			found = True
  
	return prime


def  calculateEncryptKey(): 
	"""
	
		Description:
		--------------
		Function calculates Encryption key E, using the standard mechanism of p,q two prime numbers, ɸ & thus calculating E 

		
		Returned Values:
		----------------
		returns calculated E and Phi for decryption key calculation

	"""
	p = nextPrime(sums)
	q = nextPrime(p)

	print("The first prime number : p = "+ str(p))
	print("The second prime number : q = "+ str(q))
	print("")

	n = p * q
	fi = (p-1) * (q-1)

	print("Calculated n = " + str(n))
	print("Calculated fi(n) = " + str(fi)) 

	encKeysList=list()

	for i in range(2, fi,1): 
		if( math.gcd(i, fi) == 1 and isPrime(i) ):
			encKeysList.append(i)
			if len(encKeysList) >= 20:
				return (encKeysList,fi)

	return (encKeysList,fi)		

def calculateDecryptKey(encKeysList, fi):
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
				if (isPrime(decKey)):
					return (encKey,decKey)



def main():

	"""
		Description:
		--------------
		Execution point of program

	"""

	encKeysList,fi=calculateEncryptKey()
	print("Encryption keys top 20 List : "+ str(encKeysList));
	encryption_key, decryption_key = calculateDecryptKey(encKeysList, fi);
	print("Encryption key e : "+ str(encryption_key));
	print("Decryption key d : " + str(decryption_key));



if __name__ == '__main__':
	main()
