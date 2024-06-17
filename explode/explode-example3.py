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

import linguistics
import pattern
from pattern.en import wordnet
explode = ximport("explode")

cellsize = 900
halfsize = int( cellsize / 2 )

size( cellsize, cellsize )

font("Arial", 10)
fill(0.2)
strokewidth(0.5)

longlistwords = (
    "container", "proponent", "car", "being", "animal",
    "human", "ape", "organism" )

nouns = list( wordnet.NOUNS() )

def setup():
    background( 0.31 )


speed(0.25)


def draw():
    background( 0.71 )
    hypolen = 0
    while hypolen < 2:
        root = choice( nouns )
        # root = choice( longlistwords )
        # root="dupe"
        # root="bird"
        # root="protestamt_denomination"
        synset = wordnet.synsets( root )[0]
        hyponyms = list( synset.hyponyms() )
        hypolen = len( hyponyms )

    synsets = wordnet.synsets( root ) 
    synset = synsets[0]
    #pp( dir(synset) )
    hyponyms = list( synset.hyponyms() )
    reset()
    translate(halfsize, halfsize)
    scale(0.45)
    explode.explode(root, hyponyms, 0,0 )

    print( """WordNet definition for '%s': "%s".""" % (root, synset.gloss ) )

