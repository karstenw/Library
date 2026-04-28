
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""


import pdb
import pprint
pp = pprint.pprint

import linguistics
FlowerWord = linguistics.FlowerWord.FlowerWord

import pattern

f = FlowerWord("house")
print("\nsynsets:", f.synsets)
s = f.synsets[0]

# pdb.set_trace()

print(s)
print()
print("\ns.antonym:", s.antonym)

print("\ns.gloss:", s.gloss)

print("\ns.hypernym:", s.hypernym)

print("\ns.part_of_speech:", s.part_of_speech)

print("\ns.pos:", s.pos)

print("\nf.senses:", f.senses())

print("\ns.synonyms:", s.synonyms)

print("\ns.tag:", s.tag)

print("\ns.weight:", s.weight)

print("\ns.holonyms:", s.holonyms())
print("\ns.hypernyms:", s.hypernyms())
print("\ns.hyponyms:", s.hyponyms())

print("\ns.meronyms:", s.meronyms())
print("\ns.similar:", s.similar())
print("\nf.holonyms:", f.holonyms())
print("\n")
#pp(dir(s))
