# PROPORTION
# A proportion defines the way rows and columns in the grid are organised.
# Here's a handy script to try out different proportions:

try: 
    grid = ximport("grid")
except:
    grid = ximport("__init__")
    reload(grid)

import itertools

speed(5)

def setup():
    pass

roundabout = itertools.cycle( range(1, 19) )

def draw():
    i = roundabout.next()
    p = grid.proportion(
        distribution="fib",
        mirrored=False,
        reversed=False,
        shuffled=False,
        sorted=False,
        repetition=1
    )
    print i
    p.generate(i)
    p.draw(10, 10, 500, 900)