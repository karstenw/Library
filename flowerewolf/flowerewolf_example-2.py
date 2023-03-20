# Note: you'll also need the NodeBox English Linguistics library:
# old: http://nodebox.net/code/index.php/Linguistics
# new: https://github.com/karstenw/linguistics

from random import seed, sample

flowerewolf = ximport("flowerewolf")

size( 800, 900 )
fontsize(24)

# select 13 random fonts
fonts = sample( fontnames(), 13 )

var("topic", TEXT, "kiss" )

flowerewolf.dada(
        str(topic), 
        foreground=color(1,1,1,0.9),
        background=color(1,0,0), 
        fonts=fonts)
