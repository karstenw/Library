# Note: you'll also need the NodeBox English Linguistics library:
# old: http://nodebox.net/code/index.php/Linguistics
# new: https://github.com/karstenw/linguistics

from random import seed, sample

# seed(1)

try:
    flowerewolf = ximport("flowerewolf")
except:
    flowerewolf = ximport("__init__")
    reload(flowerewolf)

var("topic", TEXT, "kiss")
size( 600, 700 )

fontsize(16)

if 0:
    fonts = ["Georgia-Bold", "Helvetica", "ArialNarrow"]
else:
    # select 13 random fonts
    fonts = sample( fontnames(), 13 )

flowerewolf.dada(
        str(topic), 
        foreground=color(1,1,1), background=color(1,0,0), 
        fonts=fonts)

