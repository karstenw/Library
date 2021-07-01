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
size(1400,1400)
wordnet = ximport("wordnet")
explode = ximport("explode")
reload(explode)

font("Arial", 10)
fill(0.2)
strokewidth(0.5)

root = "container"
explode.explode(root, wordnet.hyponyms(root), 700, 700)

print( "WordNet definition for " + root + ": " + wordnet.gloss(root) )