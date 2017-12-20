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
    if n < 2:
        return False
    # check the list of primes
    if n in primesList:
        return True
    # n is either composite and smaller than the largest prime in the primes list
    # or n is a number greater than the greatest prime in the primes list
    if n <= primesList[-1]:
        i = 0
        while primesList[i] <= n:
            if n % primesList[i] == 0:
                return False
            i += 1
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

# Return the number of primes that divide n
def numberOfPrimeDivisors(n):
   primes, multiplicities = factorize(n)
   return len(primes)

# Return the sum of the exponents of the prime factorization of n
def multiplicityOfPrimes(n):
   primes, multiplicities = factorize(n)
   return sum(multiplicities)
   
# Factorize positive integer n into primes and corresponding multiplicities
def factorize(n):
    if not n in factorizationMap.keys():
        primes = []
        multiplicities = []
        exponent = 0
        if n < primesList[-1]:
            # use the primes list
            primeRange = primesList
        else:
            primeRange = primesInRange(2, n)
        for prime in primeRange:
            if prime > n:
                break
            saved = n
            while n % prime == 0:
                n /= prime
                exponent += 1
            n = saved
            if exponent > 0:
                primes.append(prime)
                multiplicities.append(exponent)
                exponent = 0
        factorizationMap[n] = primes, multiplicities     
    return factorizationMap[n]

# Compute the positive divisors of n
def divisors(n):
    if not n in divisorsMap.keys():
        divisorsMap[n] = [d for d in range(1, n+1) if n % d == 0]
    return divisorsMap[n]

# Calculate Euler's totient function at n - this is the number of 
# positive integers less than n which are relatively prime to n
def eulerTotient(n):
   primes, multiplicities = factorize(n)
   num = reduce(mul, [(prime - 1) for prime in primes], 1)
   den = reduce(mul, primes, 1)
   return n * num / den

# Generate kth Jordan totient function - a generalization of Euler's
def jordanTotient(k):
   def jordanTotient_k(n):
      primes, multiplicities = factorize(n)
      num = reduce(mul, [(prime**k - 1) for prime in primes], 1)
      den = reduce(mul, [prime**k for prime in primes], 1)
      return n**k * num / den
   return jordanTotient_k

# Generate function which returns the sum of kth powers of the divisors of n
# Note: sigma_k(n, 0) = tau(n), sigma_k(n, 1) = sigma(n)
def sigma(k):
   def sigma_k(n):
      return sum([divisor**k for divisor in divisors(n)])
   return sigma_k

# Returns a function which is the Dirichlet convolution of f and g
def dirichletConvolution(f, g):
    def convolution(n):
        return sum([f(d)*g(n/d) for d in divisors(n)])
    return convolution

# Returns a function which is the composition of f and g
def compose(f, g):
    def composition(n):
        return f(g(n))
    return composition

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