import math 


name = input("PLease Enter the Name: ")  
print("\n")

l1=[character for character in name]  
l2=[ord(character) for character in name]

print(l1)
print(l2)
print("\n")

sum = 0
for num in l2:
    sum += num
print("Sum of ASCII value is : " + str(sum))  
print("\n")


def isPrime(num):

	if num > 1: 
		for i in range(2, num,1):
			if ((num % i) == 0):
				return False
		return True

def nextPrime(N): 
  
    if (N <= 1): 
        return 2
  
    prime = N 
    found = False
  
    while(not found): 
        prime = prime + 1
  
        if(isPrime(prime) == True): 
            found = True
  
    return prime


def countGCD(L): 
	for i in range(2, L,1): 
		if( math.gcd(i, L) == 1 and isPrime(i) ):
			if i > 50:
				return i;


def calculate_d(e, L):
	for i in range(2, L,1):
		if(isPrime(i) and ((e*i) % L) == 1):
			return i




p = nextPrime(sum)
q = nextPrime(p)
print("The first prime number : p = "+ str(p))
print("The second prime number : q = "+ str(q))
print("\n")

n = p * q
fi = (p-1) * (q-1)

print("Calculated n = " + str(n))
print("Calculated fi(n) = " + str(fi)) 



encryption_key=countGCD(fi)
print("Encryption key e : "+ str(encryption_key));
decryption_key = calculate_d(encryption_key, fi);
print("Decryption key d : " + str(decryption_key));


