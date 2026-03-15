# PERCEPTION BROWSER

import pdb

perception = ximport("perception")

languageCodes = list( perception.cnr.coreLanguageCodes )
languageCodes.sort()
languageCodes.insert(0, "")
lang=""

def handler( value, name ):
    global lang, concept
    if name == 'concept':
        concept = value
    elif name == "language":
        lang = language
    load( concept, lang )
    
var("concept", TEXT, "dog", handler=handler)
var("language", MENU, default=handler, value=languageCodes)


g = None
def load( theConcept, lang="" ):
    
    global g, concept
    concept = theConcept
    # Load a new cluster of nodes surrounding the clicked node.
    # Note the "maxedges" parameter - you won't find it documented.
    # We use it here to cap the number of rules returned.
    # A fast graph is more important right now than all of the data.
    g = perception.cluster( str(theConcept), depth=2, maxedges=100, labeled=1, lang=lang)
    g.distance = 4.1
    g.layout.n = 2000
    g.styles.apply()
    g.layout.force = 0.001 # lower if nodes are twitching
    g.events.click = load
    if 1:
        print("load:", concept, len(g) )

load("Dog", 'en')

size( 1024, 1024)
if 1:
    speed(16)
    def draw():
        g.update()
        g.draw(traffic=False, directed=False)
else:
    background(0.5)