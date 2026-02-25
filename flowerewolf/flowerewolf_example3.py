# Note: you'll also need the NodeBox English Linguistics library:
# old: http://nodebox.net/code/index.php/Linguistics
# new: https://github.com/karstenw/linguistics

from random import seed, sample

flowerewolf = ximport("flowerewolf")

size( 1200, 1200 )
fontsize(24)

# select 13 random fonts

allnouns = list(flowerewolf.allnouns)
allfonts = fontnames()
speed( 0.2 )

def setup():
    pass

def draw():
    fonts = sample( allfonts, 20 )
    topic = str(choice( allnouns ))
    printtopic = topic.replace("_", " ")
    print("topic:", printtopic)
    flowerewolf.dada(
            topic,
            foreground=color(1,1,1,0.9),
            background=color(1,0,0),
            fonts=fonts,
            fontsizepts=64)
