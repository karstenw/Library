
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""


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
    if word.pos == 'v':
        verbs.append( word )
    if word.pos == 'a':
        adjectives.append( word )

s3 = time.time()
print("build wordlists %.3f" % (s3-s2) )
print("nouns: %i" % (len(nouns),) )
print("verbs: %i" % (len(verbs),) )
print("adjectives: %i" % (len(adjectives),) )



wrd = 'bird'
print("query:", wrd)
words = wn.words( wrd )
print("words:", words)
word = words[0]
print("word:", word)

senses = word.senses()
print("senses:", senses)

sense = senses[0]
print("sense:", sense)


synsets = word.synsets()
print("synsets:", synsets)

synset = synsets[0]
print("synset:", synset)

# pdb.set_trace()

# pp(dir(sense))
# 'adjposition', 'closure', 'counts', 'examples', 'frames', 'get_related',
# 'get_related_synsets', 'id', 'lexicalized', 'lexicon', 'metadata', 'relation_map',
# 'relation_paths', 'relations', 'synset', 'translate', 'word']

# pp(dir(synset))
# 'closure', 'common_hypernyms', 'definition', 'definitions', 'empty', 'examples',
# 'get_related', 'holonyms', 'hypernym_paths', 'hypernyms', 'hyponyms', 'id', 'ili',
# 'lemmas', 'lexfile', 'lexicalized', 'lexicon', 'lowest_common_hypernyms', 'max_depth',
# 'meronyms', 'metadata', 'min_depth', 'pos', 'relation_map', 'relation_paths',
# 'relations', 'senses', 'shortest_path', 'translate', 'words']


#synonyms = w.synsets()
#antonyms = w.antonyms()
#lemmasynonyms = [t.lemmas()[0] for t in synonyms]

if 1:
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
print("synset demo %.3f" % (s4-s1) )

