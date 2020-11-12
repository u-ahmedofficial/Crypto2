# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:06:54 2020

@author: laiba
"""
import math

# Calculating ACII Sum
sum=0
name_A = input("Enter your name in capital: ")
for i in range(0,len(name_A),1):
    sum = sum + ord(name_A[i])
    
print("The ASCII sum for " + name_A + " is: " ,sum)


#Checking Prime Function
def isPrime(n) : 
  
    # Corner cases 
    if (n <= 1) : 
        return False
    if (n <= 3) : 
        return True
  
    # This is checked so that we can skip  
    # middle five numbers in below loop 
    if (n % 2 == 0 or n % 3 == 0) : 
        return False
  
    i = 5
    while(i * i <= n) : 
        if (n % i == 0 or n % (i + 2) == 0) : 
            return False
        i = i + 6
  
    return True

#Calculating p
cal_p=sum+1
found= True
while(found):
    if(isPrime(cal_p)):
        print(cal_p, "is a prime number")
        p= cal_p
        print("So,p = ", p)
        break
    else:
        cal_p=cal_p+1
        
#Calculating q        
cal_q = cal_p + 1
while(found):
    if(isPrime(cal_q)):
        print(cal_q, "is a prime number")
        q= cal_q
        print("So,q = ", q)
        break
    else:
        cal_q=cal_q+1
        
#Calculating n
n= p * q
print("Value of n is: ", n)

#Calculating phi-n
phi_n = (p-1) * (q-1)
print("Value of ϕ(n) is: ", phi_n)

#Calculating e
cal_e=2
while(cal_e>1 & cal_e<phi_n):
    if math.gcd(cal_e, phi_n) == 1:
       e = cal_e
       print("The Value of e is: ",e) 
       
       break
    else:
       cal_e = cal_e+1
       
#Calculating d
cal_d=2
while(cal_d>1 & cal_d<phi_n):
    if (cal_d * e % phi_n) == 1:
       d= cal_d
       print("The Value of d is: ",d) 
       break
    else:
       cal_d = cal_d+1
       
    



