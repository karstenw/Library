# PERCEPTION BROWSER

try:
    perception = ximport("perception")
except ImportError:
    perception = ximport("__init__")
    reload(perception)

g = None
def load(node, lang="en"):
    
    global g
    # Load a new cluster of nodes surrounding the clicked node.
    # Note the "maxedges" parameter - you won't find it documented.
    # We use it here to cap the number of rules returned.
    # A fast graph is more important right now than all of the data.
    g = perception.cluster(str(node), depth=2, maxedges=999, labeled=1, lang=lang)
    g.distance = 2.8
    g.layout.n = 2000
    g.styles.apply()
    g.layout.force = 0.001 # lower if nodes are twitching
    g.events.click = load

targets = (
    ("House", 'en'),
    ("Casa", "it"),
    ("Huis", "nl"),
    ("Maison", "fr"),
    ("Haus", "de"),
    ("Nada", "es"),
    ("domus", "la"))

p = choice( targets )
print( p )
load( *p )


size(850, 850)
speed(60)
def draw():
    g.update()
    g.draw(traffic=True, directed=True)


