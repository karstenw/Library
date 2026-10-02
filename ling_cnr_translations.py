
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""


import sys
import os
import pprint
pp=pprint.pprint
import pdb
from pathlib import Path

import linguistics
import conceptnetreader as cnr


lang2 = False

if len(sys.argv) == 0:
    #lang = 'de'
    #args = ['Haus',]
    lang = 'fr'
    args = ['Maison',]

elif len(sys.argv) == 3:
    lang = sys.argv[1]
    args = sys.argv[2:]

elif len(sys.argv) > 3:
    lang = sys.argv[1]
    lang2 = sys.argv[2]
    args = sys.argv[3:]

#pp(cnr.relationnames)

#pp(cnr.languagenames)


for word in args:
    concepts, resultconcepts = cnr.query_translations( word, lang, weight=0.0 )
    print()
    print("word:", word)
    for concept in resultconcepts:
        if lang2 and lang2 != concept.concept2lang:
            continue
        print(concept.concept1name, concept.concept1lang,
              concept.relationname,
              concept.concept2name, concept.concept2lang,
              concept.weight )
    print("\n\n" + "-"*40 + "\n\n")


