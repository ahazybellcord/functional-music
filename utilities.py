from operator import mul
from math import *
from random import *
from re import match

# Global map to hold factorizations of integers up to upperLimit
factorizationMap = {}
# Global map to hold divisors of integers up to upperLimit
divisorsMap = {}
# Global list to hold prime numbers up to 10*upperLimit
primesList = []
upperLimit = 10000

# Normalize the given sequence to within interval [loNorm, hiNorm]
def normalizeRange(sequence, normRange):
   lo, hi = min(sequence), max(sequence)
   loNorm, hiNorm = normRange[0], normRange[1]
   N = len(sequence)
   # sequence may be constant - then return middle of normalized range
   if hi-lo == 0:
      return [(hiNorm+loNorm)/2 for i in range(N)]
   return [float(hiNorm-loNorm)*(sequence[i]-lo)/(hi-lo)+loNorm for i in range(N)]

# Return the values of given function fn from input values lo to hi
def valuesInRange(fn, lo, hi):
   return [fn(n) for n in range(lo, hi+1)]

# Return the cumulative sum of function values from lo to hi
def cumulativeSumValuesInRange(fn, lo, hi):
   values = valuesInRange(fn, lo, hi)
   return [sum(values[0:i]) for i in range(1,hi+1)]

# Return the first n consecutive positive integers
def identity(n):
   return n

# Return 1
def one(n):
   return 1

# Return a random number in range [0, 127]
def rnd(n):
   return randrange(128)

# Return nth triangular number
def triangle(n):
   return n*(n+1)/2

# Return nth square 
def square(n):
   return n**2

# Return nth cubic number
def cube(n):
   return n**3

# Primality test - return True if n is prime, False otherwise
def isPrime(n):
    # first prime is 2, check for even to eliminate half the input
    if n < 2 or (n > 2 and n % 2 == 0):
        return False
    # check the list of primes
    if n == 2 or n in primesList:
        return True
    # if n is within the range of primesList, loop over the primes
    # and see if any divide into n
    if len(primesList) > 0:
        if n < primesList[-1]:
            for prime in primesList:
                if prime > n:
                    break
                if n % prime == 0:
                    return False
    else:
        # otherwise check over all odd numbers up to n
        for d in range(3, n, 2):
            if n % d == 0:
                return False
    return True

# Return list of primes in range [lo, hi]
def primesInRange(lo, hi):
    primes = []
    for p in range(lo, hi+1):
        if isPrime(p):
            primes.append(p)
    return primes
 
# Return 2 if n is prime, 1 otherwise
def isPrimeYesNo(n):
   if isPrime(n):
      return 2
   return 1
 
# Factorize positive integer n into primes and corresponding multiplicities
def factorize(n):
    number = n
    if not n in factorizationMap.keys():
        primes = []
        multiplicities = []
        exponent = 0
        if len(primesList) > 0 and n < primesList[-1]:
            # use the primes list
            primeRange = primesList
        else:
            primeRange = primesInRange(2, n)
        for prime in primeRange:
            if prime > n:
                break
            while n % prime == 0:
                n /= prime
                exponent += 1
            if exponent > 0:
                primes.append(prime)
                multiplicities.append(exponent)
                exponent = 0
        factorizationMap[number] = primes, multiplicities     
    return factorizationMap[number]

# Compute the positive divisors of n
def divisors(n):
    if not n in divisorsMap.keys():
        divisorsMap[n] = [d for d in range(1, n+1) if n % d == 0]
    return divisorsMap[n]

# Calculate Euler's totient function at n - this is the number of 
# positive integers less than n which are relatively prime to n
# From closed-form definition found on p. 145 of Burton
def totient(n):
   if not n in factorizationMap.keys():
      factorize(n)
   primes, multiplicities = factorizationMap[n]

   num = reduce(mul, [prime - 1 for prime in primes], 1)
   den = reduce(mul, primes, 1)
   return n * num / den

# Returns number of positive divisors of n
def tau(n):
   if not n in divisorsMap.keys():
      divisors(n)
   return len(divisorsMap[n])

# Return the sum of the positive divisors of n
def sigma(n):
   if not n in divisorsMap.keys():
      divisors(n)
   return sum(divisorsMap[n])

# Returns a function which is the Dirichlet convolution of f and g
def dirichletConvolution(f, g):
    def convolution(n):
        if not n in divisorsMap.keys():
            divisors(n)
        divisorsOfN = divisorsMap[n]
        # d surely divides n and so n/d is an integer
        return sum([f(d)*g(n/d) for d in divisorsOfN])
    return convolution

# Returns a function which is the composition of f and g
def compose(f, g):
    def composed(n):
        return f(g(n))
    return composed

# For computational efficiency, store the factorizations of numbers up to upperLimit in a 
# global map built from a look-up table (text file) in project directory
def buildFactorizationMap():
   with open('factorizations.txt', 'r') as factorizations:
      for line in factorizations:
         matchObj = match('(?P<number>\d+)\[(?P<primesMatch>(\d+)?(,\d+)*\])(?P<multiplicitiesMatch>(\d+)?(,\d+)*)', line)
         if int(matchObj.group('number')) == 1:
            factorizationMap[1] = [], []
            continue
         
         primes = []
         matchedPrimes = matchObj.group('primesMatch')
         currentPrime = []
         for i in range(len(matchedPrimes)):
            if matchedPrimes[i] == ' ':
               continue
            if matchedPrimes[i] in [',',']']:
               primes.append(int(''.join(currentPrime)))
               currentPrime = []
            else:
               currentPrime.append(matchedPrimes[i])
          
         multiplicities = []
         matchedMultiplicities = matchObj.group('multiplicitiesMatch')
         currentMultiplicity = []
         for i in range(len(matchedMultiplicities)):
            if matchedMultiplicities[i] == ' ':
               continue
            if matchedMultiplicities[i] in [',','\n']:
               multiplicities.append(int(''.join(currentMultiplicity)))
               currentMultiplicity = []
            else:
               currentMultiplicity.append(matchedMultiplicities[i])

         factorizationMap[int(matchObj.group('number'))] = primes, multiplicities
         

# For computational efficiency, store the divisors of numbers up to upperLimit in a global 
# map built from a look-up table (text file) in project directory
def buildDivisorsMap():
   with open('divisors.txt', 'r') as divisors:
      for line in divisors:
         matchObj = match('(?P<number>\d+)\[(?P<divisorsMatch>(\d+)?(,\d+)*\])', line)

         div = []
         matchedDivisors = matchObj.group('divisorsMatch')
         currentDivisor = []
         for i in range(len(matchedDivisors)):
            if matchedDivisors[i] == ' ':
               continue
            if matchedDivisors[i] in [',',']']:
               div.append(int(''.join(currentDivisor)))
               currentDivisor = []
            else:
               currentDivisor.append(matchedDivisors[i])
         
         divisorsMap[int(matchObj.group('number'))] = div

# For computational efficiency, store prime numbers up to 10*upperLimit in a global 
# list built from a look-up table (text file) in project directory
def buildPrimesList():
   with open('primes.txt', 'r') as primes:
      for line in primes:
         primesList.append(int(line))