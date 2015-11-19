springgraph = ximport("springgraph")
reload(springgraph)

from time import time

size(400, 400)

# A graph object.
g = springgraph.graph(iterations=500, distance=1.0)

# Graph properties:
#
# Graph(iterations=500, distance=1.0)            # creates a new graph
#
# g.nodes                                        # a list of node objects (with .x, .y, .connections())
# g.edges                                        # a list of edge objects (with .id1, .id2, .weight)
# g.layout.iterations                            # the number of iterations to calculate
# g.layout.max_repulsive_force_distance
# g.layout.max_vertex_movement
#
#
# g.add_node(node_id, radius=8, style="")        # adds a node
# g.add_edge(node_id1, node_id2, weight=None)    # adds a (weighted) edge
# g.remove_node(node_id)                         # removes a node object and its edges
# g.find(node_id)                                # returns a node object
# g.update()                                     # calculate next layout iteration
# g.center()                                     # centers the graph on the canvas
# g.distance_from_center(node_obj)               # absolute distance between 2 nodes
# g.draw(dx=0, dy=0, highlight=[])               # draws the graph to the canvas
# g.mouse_inside(node_obj)                       # is the mouse over the node?
# g.drag(node_obj)                               # drag node to mouse location in animation
# g.events()                                     # listens to user interaction
# g.distance_map()                               # returns {id1: [{id2:0.2}, {id3:0.3}, ...]}
# g.shortest_path(node_id1, node_id2)            # returns a list of node id's

from random import seed
seed(6)

for i in range(40):
    # Add nodes with a random id.
    id = random(500)
    if not id in g.index.keys():
        g.add_node(id)
        # Connect to random other nodes.
        if random() > 0.5:
            for i in range(choice((2,3))):
                n = choice(g.nodes)
                if id != n.id:
                    g.add_edge(id, n.id)

# Redefine the coloring for shortest paths.
g.styles.highlight.stroke = color(1, 1, 0)
# Set a property on all styles:
#g.styles.text = None

# Connect orphans to the first node.
for n in g.nodes:
    if (len(n.links)) == 0:
        n.style = "light"
        g.add_edge(choice(g.nodes[0:2]).id, n.id, weight=1.0)

# Colorize nodes.
# Nodes with higher traffic are blue.
first = True
for n in g.nodes:
    if len(n.links) > 4:
        n.style = "blue"
    if first:
        first = False
        n.style = "root"

# Update the graph until it's done.
# Each update, the position of nodes is improved
# based on attractive and repulsive forces.
g.solve()

#print springgraph.brandes_betweenness_centrality(g.distance_map(), g.index.keys())

# If the graph is completely calculated
# (according to the number of iterations),
# show shortest path between random nodes.
path = []
if g.update() == False:
    id1 = choice(g.index.keys())
    id2 = choice(g.index.keys())
    path = g.shortest_path(id1, id2)

print g.distance_map()
print springgraph.centrality(g)
print g.strongest_nodes()

# Draw the graph
# and display the shortest path.
g.draw(highlight=path)
