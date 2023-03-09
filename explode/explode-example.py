# WordNet and Explode-grapher example
# Author: Tom De Smedt <tomdesmedt@trapdoor.be>
# Manual: http://nodebox.net/code/index.php/WordNet
# http://nodebox.net/code/index.php/Explode
# Copyright (c) 2005 by Tom De Smedt.
# Usage is free for non-commercial use:
# refer to the "Use" section on http://nodebox.net/code

# This example imports both WordNet and Explode.
# Place this file along with explode.py in the WordNet folder,
# next to wordnet.py and the pywordnet folder.


import pprint
pp=pprint.pprint

# wordnet = ximport("wordnet")
from pattern.en import wordnet
explode = ximport("explode")
# reload(explode)


cellsize = 900
halfsize = int( cellsize / 2 )
size( cellsize, cellsize )
background( 0.89 )

font("Arial", 10)
fill(0.2)
strokewidth(0.5)

longlistwords = (
    "container", "proponent", "car", "being", "animal",
    "human", "ape" )

nouns = list( wordnet.NOUNS() )

if 1:
    hypolen = 0
    while hypolen < 2:
        root = choice( nouns )
        synset = wordnet.synsets( root )[0]
        hyponyms = list( synset.hyponyms() )
        hypolen = len( hyponyms )
else:
    root = "container"


synsets = wordnet.synsets( root ) 
synset = synsets[0]
#pp( dir(synset) )
hyponyms = list( synset.hyponyms() )

explode.explode(root, hyponyms, halfsize, halfsize)

print( """WordNet definition for '%s': "%s".""" % (root, synset.gloss ) )
