import math




def isprime(num):

	if num > 1: 
		for i in range(2, num,1):
			if ((num % i) == 0):
				return False
		return True


def countGCD(L): 
	for i in range(2, L,1): 
		if( math.gcd(i, L) == 1 and isprime(i) ):
			if i > 50:
				return i;



def calculate_d(e, L):
	for i in range(2, L,1):
		if (((e*i) % L) == 1):
			if isprime(i):
				
				return i;



	
					
print(calculate_d(3,429016))
	
# L = 429016

# encryption_key=countGCD(L)
# print("Encryption key e : "+ str(encryption_key));
# decryption_key = calculate_d(encryption_key, L);
# print("Decryption key d : " + str(decryption_key));





