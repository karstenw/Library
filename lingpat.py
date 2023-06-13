
import sys,os,pprint,pdb,time
pp=pprint.pprint

s1 = time.time()
import linguistics

s2 = time.time()
print("import linguistics %.3f" % (s2-s1) )

import pattern
import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = en.wordnet

s3 = time.time()
print("import pattern %.3f" % (s3-s2) )


# pdb.set_trace()

synsets = wordnet.synsets('dog')
s = synsets[0]
print( '    synset:', s )
print( '     gloss:', s.gloss )
print( '    senses:', s.senses )
print( '  synonyms:', s.synonyms )
print( '   antonym:', s.antonym )
print( '   lexname:', s.lexname )

print(  )
print( ' Hypernyms:', s.hypernyms() )
print( '  Hyponyms:', s.hyponyms() )
print( '  Holonyms:', s.holonyms() )
print( '  Meronyms:', s.meronyms() )
print(  )

s4 = time.time()
print("synset demo %.3f" % (s4-s3) )

if 0:
    allnouns = set( wordnet.NOUNS())
    misses = {}
    for noun in allnouns:
        ss = wordnet.synsets( noun )[0]
        if ss.synonyms[0] != noun:
            if noun in ss.synonyms:
                continue
            lower = [t.lower() for t in ss.synonyms]
            if noun in lower:
                continue
            if noun not in misses:
                misses[noun] = []
            misses[noun].extend( ss.synonyms )
    print("##misses:", len(misses) )

    s5 = time.time()
    print("check all synsets %.3f" % (s5-s4) )


#import nltk
#import nltk.corpus
#from nltk.corpus.reader.framenet import PrettyList
#fn = import nltk.corpus.framenet


import perception
pdb.set_trace()
q = perception.cluster("cool", depth=2, maxedges=30, labeled=False)
print( q )
