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
speed(5)

def setup():
    pass

wordnet = ximport("wordnet")
explode = ximport("explode")
reload(explode)

nouns = wordnet.wn.N.keys()
root = "container"
# root = choice( nouns )
hyponyms = wordnet.hyponyms(root)
hyponyms.sort()

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