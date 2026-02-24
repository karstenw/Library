import sys
import os
import pprint
pp=pprint.pprint
import pdb
from pathlib import Path

import linguistics
import conceptnetreader as cnr


if 1:
    print( "cnr.databasefile:", cnr.databasefile )

    print( "#languages:", len(cnr.languages) )
    print( "#relations:", len(cnr.relations) )
    print( "#contexts:", len(cnr.contexts) )
    # pp( cnr.relations )

# pdb.set_trace()

if len(sys.argv) > 2:
    lang = sys.argv[1]
    args = sys.argv[2:]
else:
    lang = 'de'
    args = ['Haus',]


for word in args:
    initialconcepts, resultconcepts, conceptsCache = cnr.query_concept(  word, maxedges=100, lang=lang, weight=1.0 )
    
    for concept in resultconcepts:
        print(concept.concept1name, concept.concept1lang,
              concept.relationname,
              concept.concept2name, concept.concept2lang,
              concept.weight )
    print("\n\n" + "-"*40 + "\n\n")


