
"""
These ling*.py scripts (ling_cnr_query.py, ling_notwork3-pat.py, lingpat.py,
lingperception.py, lingtest.py, lingwn.py ) are my test and tryout scripts for the linguistics library.
"""

#
# ling_cnr_query.py LANGCODE WORD
#
# Dumps all edges for WORD in LANGCODE
#
# ling_cnr_query.py de Haus
#
import sys
import os
import pprint
pp=pprint.pprint
import pdb
from pathlib import Path

import linguistics
import conceptnetreader as cnr


if 0:
    print( "cnr.databasefile:", cnr.databasefile )

    print( "#languages:", len(cnr.languages) )
    print( "#relations:", len(cnr.relations) )
    print( "#contexts:", len(cnr.contexts) )
    # pp( cnr.relations )
    # pp( cnr.languages )
# pdb.set_trace()

if len(sys.argv) > 2:
    lang = sys.argv[1]
    args = sys.argv[2:]
else:
    lang = 'de'
    args = ['Haus',]


for word in args:
    initialconcepts, resultconcepts, conceptsCache = cnr.query_concept(
                                            word, maxedges=300, lang=lang, weight=0.0 )
    
    for concept in resultconcepts:
        s = "{0:18} {1:20} {2:32} {3:18} {4}".format(
                concept.concept1name, concept.concept1langname,
                concept.relationname,
                concept.concept2name, concept.concept2langname)
        print( s )
        # print( concept )
    print("\n\n" + "-"*40 + "\n\n")


