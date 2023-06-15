
import time
s1 = time.time()

import sys,os,pprint,pdb
pp=pprint.pprint

import linguistics
import wn

s2 = time.time()
print("import linguistics & wn %.3f" % (s2-s1) )



# pdb.set_trace()



nouns = []
verbs = []
adjectives = []
for word in wn.words(lang="en"):
    if word.pos == 'n':
        nouns.append( word )
    elif word.pos == 'v':
        verbs.append( word )
    elif word.pos == 'a':
        adjectives.append( word )

s3 = time.time()
print("buikd wordlists %.3f" % (s3-s2) )


synsets = wn.synsets('bird')
s = synsets[0]
w = s.words()[0]
synonyms = w.synsets()
lemmasynonyms = [t.lemmas()[0] for t in synonyms]


pp(synsets)

print( '    synset:', s )
print( 'Definition:', s.definition() )
print( '  Synonyms:', synonyms )
print( ' Hypernyms:', s.hypernyms() )
print( '  Hyponyms:', s.hyponyms() )
print( '  Holonyms:', s.holonyms() )
print( '  Meronyms:', s.meronyms() )
# print( '   Antonym:', s.antonym )

s4 = time.time()
print("synset demo %.3f" % (s4-s3) )

