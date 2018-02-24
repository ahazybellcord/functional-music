# Run this script if missing files 'primes.txt', 'factorizations.txt', or 'divisors.txt'
from utilities import *


# Write the list of primes, factorizations and divisors 
# to a text file as a lookup table to load on each execution
# of the project file
with open('primes.txt', 'w') as primesListFile:
    for prime in primesInRange(1, 10*upperLimit+1):
        primesListFile.write('%d\n' % prime)

for number in range(1, upperLimit+1):
    print 'Factorizing %d...' % number
    factorize(number)
    print 'Computing the divisors of %d...' % number
    divisors(number)
   
with open('factorizations.txt', 'w') as factorizationsFile:
    for number in range(1, upperLimit+1):
        primes, multiplicities = factorizationMap[number]
        primesString = str(primes).replace(' ','')
        multiplicitiesString = str(multiplicities).replace('[','')
        multiplicitiesString = multiplicitiesString.replace(']','')
        multiplicitiesString = multiplicitiesString.replace(' ','')
        factorizationsFile.write('%d%s%s\n'%(number,primesString,multiplicitiesString))

with open('divisors.txt','w') as divisorsFile:
    for number in range(1, upperLimit+1):
        divisorsFile.write('%d%s\n'%(number,str(divisorsMap[number]).replace(' ','')))

print 'Done!'