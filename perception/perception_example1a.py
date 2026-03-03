# PERCEPTION BROWSER

import pdb

try:
    perception = ximport("perception")
except ImportError:
    perception = ximport("__init__")
    # reload(perception)

g = None
def load( concept ):
    
    global g
    # Load a new cluster of nodes surrounding the clicked node.
    # Note the "maxedges" parameter - you won't find it documented.
    # We use it here to cap the number of rules returned.
    # A fast graph is more important right now than all of the data.
    g = perception.cluster( str(concept), depth=2, maxedges=65, labeled=1, lang="")
    g.distance = 2.9
    g.layout.n = 1000
    g.styles.apply()
    g.layout.force = 0.001 # lower if nodes are twitching
    g.events.click = load
    if 1:
        print("load:", concept, type(concept), len(g) )
    
        # pdb.set_trace()

load("Dog")

size( 1024, 1024)

speed(16)
def draw():
    g.update()
    g.draw(traffic=False, directed=False)
