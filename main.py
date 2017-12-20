from music import *
from math import *
from os import *
from random import *
from utilities import *


def makeComposition():
   # Build primes list and factorization and divisors maps from 
   # look-up tables (text files) for all positive integers up to 
   # upperLimit specified in utilities.py
   buildPrimesList()
   buildFactorizationMap()
   buildDivisorsMap()
   
   # total number of parts/instruments in score
   numberOfParts = randrange(3, 7)
   
   # total number of phrases per part
   # phrases between parts are coordinated to start together
   numberOfPhrases = randrange(4, 33)
   
   # functions to use as parameter controls - all defined in utilities.py
   # each function is number-theoretic, mapping positive integers to positive integers
   #fns = [identity, one, square, triangle, totient, tau, sigma, isPrimeYesNo]
   fns = [isPrimeYesNo, numberOfPrimeDivisors, multiplicityOfPrimes, sigma(0), sigma(1), sigma(2), jordanTotient(1), jordanTotient(2)]
   numberOfFunctions = len(fns)
   
   # create score
   score = Score()

   # keep track of the tempi of each part to compute the start times of each phrase
   tempi = []
   # keep track of the start times of part 1
   startTimes = [0 for i in range(numberOfPhrases+1)]
   
   for partNumber in range(numberOfParts):
      print 'Part %d/%d' % (partNumber+1, numberOfParts)
      # create part - assign a random instrument
      part = Part('Part %d' % (partNumber+1), randrange(128), partNumber)
      # assign tempo to part and save tempo to tempi array
      tempo = randrange(400, 2001)
      part.setTempo(tempo)
      tempi.append(tempo)
      
      for phraseNumber in range(numberOfPhrases):
         print 'Composing phrase %d/%d...' % (phraseNumber+1,numberOfPhrases)
         # at the phrase level
         # total number of notes in this phrase
         numberOfNotes = randrange(16, 201)
         
         # set parameter constraints for this phrase (subintervals within allowable parameter values)
         pitchRange = [randrange(32, 81), randrange(4000, 12001)] # frequencies in Hz
         durationRange = [0.0 + 0.2*random(), 1.5 + random()]
         dynamicRange = [20 + 20*random(), 110 - 40*random()]
         panRange = [0.2*random(), 1.0-0.2*random()]
         lengthRange = [0.5*random(), 1.0 - 0.4*random()]
         ranges = [pitchRange, durationRange, dynamicRange, panRange, lengthRange] 
         
         parameters = []
         # five parameters: pitch, duration, dynamics, pan, length
         for parameterNumber in range(5):
            # pick a random function for this parameter
            fn = fns[randrange(numberOfFunctions)]
            # randomly choose to compose with another function
            if random() < 0.6:
               # compose function with another randomly generated function for novelty
               fn = compose(fn, fns[randrange(numberOfFunctions)])  
            # randomly choose to compute the Dirichlet convolution with another random function
            if random() < 0.3:
               fn = dirichletConvolution(fn, fns[randrange(numberOfFunctions)])
            # randomly choose to cumulatively sum the function values
            if random() < 0.2:
               sequence = cumulativeSumValuesInRange(fn, 1, numberOfNotes)
            # or just use the function values as is
            else:
               sequence = valuesInRange(fn, 1, numberOfNotes)
            
            # normalize all number sequences to within allowable parameter ranges 
            sequence = normalizeRange(sequence, ranges[parameterNumber])
            # normalize pitch values to float so that they're treated as frequency in Hz
            if parameterNumber == 0:
               sequence = [float(sequence[i]) for i in range(numberOfNotes)] 
            # round dynamics values to integer
            if parameterNumber == 2: 
               sequence = [int(round(sequence[i])) for i in range(numberOfNotes)]
            
            # randomly select parameters to retrograde since many of the functions
            # are asymptotically increasing
            if random() < 0.5:
               sequence.reverse()
            
            parameters.append(sequence)
   
         # create phrase from computed parameters
         phrase = Phrase()
         phrase.addNoteList(*parameters)
         
         if partNumber == 0:
            # update start times to coordinate between parts
            phraseDuration = sum(parameters[1])
            startTimes[phraseNumber + 1] = startTimes[phraseNumber] + phraseDuration
   
         # coordinate this phrase to start with the corresponding phrase of part 1
         # by scaling the start time of this phrase by the tempo ratio of this part and part 1
         phrase.setStartTime(tempi[partNumber] * startTimes[phraseNumber] / tempi[0])
         
         # randomly choose to invert phrase about a MIDI note in range [40, 80]
         if random() < 0.3:
            Mod.invert(phrase, randrange(40,81))
         
         # add phrase to part
         part.addPhrase(phrase)
      
      # back to part level
      # add part to score
      score.addPart(part)
   
   # back to score level
   print 'Composition complete!'
   # play MIDI file and view graphical representation
   Play.midi(score)
   #View.pianoRoll(score)
   View.sketch(score)
   
   # save MIDI file
   name = raw_input('Enter filename to save')
   Write.midi(score,'midi/%s.mid' % name)

makeComposition()