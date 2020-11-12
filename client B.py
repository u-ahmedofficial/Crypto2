import sympy

def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a


def primRoots(modulo):
    roots = []
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)

    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            roots.append(g)           
    return roots

if __name__ == "__main__":

    #diffie_q = 787
    #diffie_q = int(input("PLease Enter the prime value of q. : "))
    diffie_q = sympy.randprime(500,1000)
    print("Value of q is :" + str(diffie_q))

    primitive_roots = primRoots(diffie_q)
    diffie_a=primitive_roots[-1]

    print("Value of alpha a : " + str(diffie_a))

    
    private_key_Xa = int(input("Enter a private key whose value is less than q : "))
    public_key_Ya = pow(diffie_a, private_key_Xa , diffie_q)
    print("Pulic key Ya : "+ str(public_key_Ya))

    #Alice_key = 203

   # secret_key = pow(Alice_key, private_key_Xa, diffie_q) 
  #print("Secret key of BOB is :" + str(secret_key))
