
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
print("build wordlists %.3f" % (s3-s2) )
print("nouns: %i" % (len(nouns),) )
print("verbs: %i" % (len(verbs),) )
print("adjectives: %i" % (len(adjectives),) )


wrd = 'bird'
w = wn.words( wrd )[0]
senses = wn.senses( wrd )
synsets = wn.synsets( wrd )

w = senses[0]
synonyms = w.synsets()
antonyms = w.antonyms()
lemmasynonyms = [t.lemmas()[0] for t in synonyms]


# pp(synsets)
print( wrd )
print( '\n    synset:', synsets )
print( '\n    senses:', senses )
# print( '\nDefinition:', w.definition() )
if 0:
    print( '\n  Synonyms:', synonyms )
    print( '\n Hypernyms:', w.hypernyms() )
    print( '\n  Hyponyms:', w.hyponyms() )
    print( '\n  Holonyms:', w.holonyms() )
    print( '\n  Meronyms:', w.meronyms() )
    print( '\n   Antonym:', antonyms )

s4 = time.time()
print("synset demo %.3f" % (s4-s3) )

