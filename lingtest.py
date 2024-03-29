import sys
import os
import pprint
pp=pprint.pprint
import pdb
from pathlib import Path

import linguistics
import linguistics.pattern
pattern = linguistics.pattern




wn = linguistics.wn
#import wn
#wn.config.data_directory = Path( os.path.abspath( './linguistics/wn-data' ) )
wordnet = wn.Wordnet( lang="en" )

allnouns = set()
allverbs = set()
alladjectives = set()

# pdb.set_trace()

missing = set()

for word in wordnet.words():
    p = word.pos
    l = word.lemma()
    if p == "n":
        allnouns.add( l )
    elif p == "v":
        allverbs.add( l )
    elif p in ("a", "s"):
        alladjectives.add( l )
    elif p == "r":
        # print("r:", l)
        pass
    else:
        missing.add( p )

if 1:
    directory = os.path.abspath('.')
    if os.path.exists( os.path.join(directory, "+private" )):
        directory = os.path.join(directory, "+private" )
    template = "%s\n"
    for p,s in ( ('allnouns.txt', allnouns),
               ('allverbs.txt', allverbs),
               ('alladjectives.txt', alladjectives)):
        path = os.path.join( directory, p )
        f = open(path,'w')
        for line in s:
            f.write( template % line )
        f.close()

    print("allnouns:", len(allnouns) )
    print("allverbs:", len(allverbs) )
    print("alladjectives:", len(alladjectives) )
