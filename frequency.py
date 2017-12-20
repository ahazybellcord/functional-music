from music import *
from math import *
from random import *
from utilities import *


lowPitch = 10 #A0
highPitch = 127 #C8
totalRange = highPitch - lowPitch + 1

# number of notes
N = 100


# Create sequences for composition parameters

frequencies = primesInRange(2,N)
frequencies = [1000*frequencies[i] for i in range(len(frequencies))]
N = len(frequencies)
print frequencies
print N
print('Building factorization map...')
buildFactorizationMap(N)
print('Building divisorMap...')
buildDivisorsMap(N)
pitches = [0 for i in range(N)]
#durations = [randrange(1,8)/8.0 for i in pitches]
durations = [EN for i in range(N)]
#durations = mertens(N)
#durations = [randrange(1,7) for i in pitches]
dynamics = [60 for i in range(N)]
#dynamics = mobius(N)
pannings = [0.3*random()+0.5 for i in range(N)]
lengths = [0.9 for i in range(N)]
lengths = [0.3*random()+0.5 for i in range(N)]

parameters = [pitches, durations, dynamics, pannings, lengths, frequencies]
# specify ranges over which to normalize parameters
ranges = [[lowPitch,highPitch],[0.25,1],[0,127],[0.0,1.0],[0.0,1.0],[40,4000]]
for i in range(len(parameters)):
   parameters[i] = normalizeRange(parameters[i], ranges[i][0], ranges[i][1])

phrase = Phrase()
phrase.addNoteList(*parameters[:-1])
phrase.setInstrument(PIANO)
phrase.setTempo(800)
notes = phrase.getNoteList()
for i in range(len(notes)):
   notes[i].setFrequency(parameters[-1][i])

part = Part(phrase)
score = Score(part)
Mod.shake(score, 20)
#Mod.tiePitches(score)
Write.midi(score,'primesupto100.mid')

Play.midi(phrase)
Play.midi(phrase)
View.sketch(phrase)
