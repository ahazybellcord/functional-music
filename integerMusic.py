from music import *
from math import *
from random import *
from utilities import *


# set parameter constraints (subintervals within allowable parameter values)
# piano range: [A0, C8] ??
pitchRange = [randrange(0,20), randrange(C6,C8)]
durationRange = [0.0, random() + 1]
dynamicRange = [10, 120]
panRange = [0.1, 0.9]
lengthRange = [0.0, 1.0]
ranges = [pitchRange, durationRange, dynamicRange, panRange, lengthRange]

tempo = randrange(100, 400)
print 'Tempo: %d bpm' % tempo

# total number of notes in each part
numberOfNotes = randrange(50,501)
# total number of parts/instruments
numberOfParts = randrange(1,4)
# total number of phrases in each part
numberOfPhrases = randrange(3,4)

# For computational efficiency, store factorizations and divisors
# of all integers up to number of notes since they will most likely 
# be used several times
print('Computing factorizations for all integers up to %d...' % numberOfNotes)
buildFactorizationMap(numberOfNotes)
print('Computing divisors for all integers up to %d...' % numberOfNotes)
buildDivisorsMap(numberOfNotes)

# functions to use as parameter controls
fns = [identity, squares, triangles, totient, totientSum, tau, sigma, rnd]

# create score
score = Score()

parts = []
for i in range(numberOfParts):
   print 'Part %d' % (i+1)
   phrases = []
   phraseDuration = 0
   for j in range(numberOfPhrases):
      print '-- Phrase %d' % (j+1)
      # Compute sequences for composition parameters
#      pitches = fns[randrange(1,len(fns))](numberOfNotes)
#      durations = fns[randrange(len(fns))](numberOfNotes)
#      dynamics = fns[randrange(len(fns))](numberOfNotes)
#      pannings = fns[randrange(len(fns))](numberOfNotes)
#      lengths = fns[randrange(len(fns))](numberOfNotes)

      ### normalize all number sequences to within allowable parameter ranges ###
      parameters = []
      for i in range(5):
         sequence = fns[randrange(len(fns))](numberOfNotes)
         parameters.append(normalizeRange(sequence, ranges[i]))

      # randomly select parameters to retrograde since most functions increase
      for parameter in parameters:
         if random() < 0.4:
            parameter.reverse()

      # phrases begin one after the other
      phrase = Phrase(phraseDuration)
      # increment part duration by the total duration of this part
      phraseDuration += sum(parameters[1])
      print 'phraseDuration: ', phraseDuration
      # create phrase and add notes
      phrase.addNoteList(*parameters)
      # set phrase tempo
      phrase.setTempo(tempo)
      # add phrase to phrase list
      phrases.append(phrase)
   
   # randomly select phrases to invert
#   for phrase in phrases:
#      if random() < 0.3:
#         Mod.invert(phrase, randrange(50,70))
#      
   # create part from phrase
   part = Part(phrases)
   # set instrument
   part.setInstrument(randrange(128))
   # add part to part list
   parts.append(part)
# create score from part list
score.addPartList(parts)

# randomize dynamics by +/-10 for humanization effect
# Mod.shake(score, 10)

# play MIDI file and view graphical representation
Play.midi(score)
View.sketch(score)
View.pianoRoll(score)

# save MIDI file
name = raw_input('Name? > ')
Write.midi(score,'%s.mid' % name)
