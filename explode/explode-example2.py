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

#size(1600,1900)
size(1800,900)
speed(5)

def setup():
    pass

# wordnet = ximport("pattern.text.en.wordnet")
explode = ximport("explode")
# reload(explode)

import linguistics
# import linguistics.pattern
# import linguistics.pattern.en
from pattern.en import wordnet
# from pattern.en import NOUN, VERB

nouns = list( wordnet.NOUNS() )

hypolen = 0
while hypolen < 2: #'_' in root or hypolen < 2:
    root = choice( nouns )
    synset = wordnet.synsets( root )[0]
    hyponyms = list( synset.hyponyms() )
    hypolen = len( hyponyms )


print("root:", root)
print("hyponyms:", hyponyms)

phi = 0

def draw():
    global phi
    push()
    scale( .33 )
    translate(1200, 1000)
    phi += 1
    font("Arial", 16)
    fill(0.2)
    strokewidth(0.5)
    rotate( phi )
    explode.explode(root, hyponyms, 0, 0, shuffleNodes=0)
    pop()

# print "WordNet definition for " + root + ": " + wordnet.gloss(root)
# draw()
