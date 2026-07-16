
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""


import pdb
import pprint
pp = pprint.pprint

import linguistics
import pattern
from FlowerWord import FlowerWord



query = "plane"
print("query:", query)

f = FlowerWord( query )
print("\nquery.synsets:", f.synsets)
s = f.synsets[0]
print("\nsynset[0]", s)

# pdb.set_trace()

print("\ns.antonym:", s.antonym)

print("\ns.gloss:", s.gloss)

print("\ns.hypernym:", s.hypernym)

print("\ns.senses:", s.senses)

print("\ns.synonyms:", s.synonyms)

print("\ns.part_of_speech:", s.part_of_speech)

print("\ns.pos:", s.pos)

print("\ns.tag:", s.tag)

print("\ns.weight:", s.weight)

print("\ns.holonyms:", s.holonyms())
print("\ns.hypernyms:", s.hypernyms())
print("\ns.hyponyms:", s.hyponyms())

print("\ns.meronyms:", s.meronyms())
print("\ns.similar:", s.similar())
print("\nf.holonyms:", f.holonyms())
print("\n")
f.print()
#pp(dir(s))
