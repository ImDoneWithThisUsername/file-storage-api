# %%
import random

# %%
def gcd(a: int, b: int):
    if a == 0:
        return b
    return gcd(b%a, a)

# %%
def power_mod(m:int, e:int, n:int):
 
    # Initialize result
    res = 1
 
    while (e > 0):
 
        # If y is odd, multiply x with result
        if ((e & 1) != 0):
            res = res * m
 
        # y must be even now
        e = e >> 1  # y = y/2
        m = m * m  # Change x to x^2
 
    return res % n

# %%
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


# %%
def nBitRandom(n:int):
   
    # Returns a random number
    # between 2**(n-1)+1 and 2**n-1'''
    return(random.randrange(2**(n-1)+1, 2**n-1))


# %%
def getLowLevelPrime(n:int):
    '''Generate a prime candidate divisible
      by first primes'''
   
    # Repeat until a number satisfying
    # the test isn't found
    while True: 
   
        # Obtain a random number
        prime_candidate = nBitRandom(n) 
   
        for divisor in first_primes_list: 
            if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                break
            # If no divisor found, return value
            else: return prime_candidate


# %%
def isMillerRabinPassed(miller_rabin_candidate:int):
	'''Run 20 iterations of Rabin Miller Primality test'''

	maxDivisionsByTwo = 0
	evenComponent = miller_rabin_candidate-1

	while evenComponent % 2 == 0:
		evenComponent >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * evenComponent == miller_rabin_candidate-1)

	def trialComposite(round_tester):
		if pow(round_tester, evenComponent,
			miller_rabin_candidate) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * evenComponent,
				miller_rabin_candidate) == miller_rabin_candidate-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2,
					miller_rabin_candidate)
		if trialComposite(round_tester):
			return False
	return True


# %%
def generate_prime(n: int):
    while True:
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate


# %%
def generate_p_q(n:int):
    while True:
        p = generate_prime(n)
        q = generate_prime(n)
        if p != q:
            return (p,q)

# %%
def generate_key_pair(n: int):
    """
    0 <= len(message) < 2**n
    len(message) should be grater than 2**8 (for some safety)
    :return: e, d, n, z, p, q
    """
    p, q = generate_p_q(n/2)
    n = p*q
    z = (p-1)*(q-1)
    e, d = None, None
    # for i in (range(2, z)):
    #     if gcd(i, z) == 1:
    #         e = i
    #         break
    while True:
        i = random.randint(2, z - 1)
        if gcd(i, z) == 1:
            e = i
            break
    for i in range(2, n):
        if (e*i - 1) % z == 0:
            d = i
            break
    return e, d, n, z, p, q

if __name__ == '__main__':
    e, d, n, z ,p , q = generate_key_pair(16)
    e, d, n, z ,p , q

    # %%
    plain = 9000
    cipher = power_mod(plain, e, n)
    plain == power_mod(cipher, d, n)


