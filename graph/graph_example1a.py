try:
    graph = ximport("graph")
except ImportError:
    graph = ximport("__init__")

size(500, 500)

g = graph.create()

# Create some relations.
g.add_edge("roof"        , "house")
g.add_edge("chimney"     , "roof")
g.add_edge("garden"      , "house")
g.add_edge("room"        , "house")
g.add_edge("kitchen"     , "room")
g.add_edge("bedroom"     , "room")
g.add_edge("bathroom"    , "room")
g.add_edge("living room" , "room")
g.add_edge("sofa"        , "living room")
g.add_edge("table"       , "living room")
g.add_edge("sink"        , "bathroom")
g.add_edge("bathtub"     , "bathroom")
g.add_edge("shower"      , "bathroom")

# Calculate a good layout.
g.solve()

# Apply default rules for node colors and size,
# for example, important nodes become blue.
g.styles.apply()

# Draw the graph, indicating the direction of each relation
# and the two nodes that get the most traffic.
g.draw(
    directed=True,
    traffic=1
)

# You'll see that "house" is the key node,
# and that "room" gets the most traffic.
