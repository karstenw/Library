
import sys,os,pprint,pdb,time
pp=pprint.pprint

s1 = time.time()
import linguistics

s2 = time.time()
print("import linguistics %.3f" % (s2-s1) )

import wn


s3 = time.time()
print("import wn %.3f" % (s3-s2) )


pdb.set_trace()



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


synsets = wn.synsets('bird')
s = synsets[0]
w = s.words()[0]
synonyms = w.synsets()
lemmasynonyms = [t.lemmas()[0] for t in synonyms]




print( '    synset:', s )
print( 'Definition:', s.definition() )
print( '  Synonyms:', synonyms )
#print( ' Hypernyms:', w.hypernyms() )
#print( '  Hyponyms:', w.hyponyms() )
#print( '  Holonyms:', w.holonyms() )
#print( '  Meronyms:', w.meronyms() )
#print( '   Antonym:', w.antonym )

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

