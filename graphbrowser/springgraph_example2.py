springgraph = ximport("springgraph")
reload(springgraph)

size(400, 400)
speed(30)

def setup():
    
    # A graph object.
    global g
    g = springgraph.graph(iterations=1000)
    
    # Add nodes with a random id.
    # Connect to random other nodes.
    for i in range(25):
        id = random(500)
        g.add_node(id)
        if random() > 0.5:
            for i in range(random(1,5)):
                n = choice(g.nodes)
                if id != n.id:
                    g.add_edge(id, n.id)
    
    # Connect orphans to the first node.
    for n in g.nodes:
        connected = False
        for e in g.edges:
            if e.node1 == n or e.node2 == n:
                connected = True
                break
        if not connected:
            n.style = "light"
            g.add_edge(g.nodes[0].id, n.id, weight=4.0)
    
    # Colorize nodes.
    # Nodes with higher traffic are blue.
    first = True
    for n in g.nodes:
        # if len(n.connections()) > 4:
        if len(n.edges) > 4:
            n.style = "blue"
        if first:
            first = False
            n.style = "root"

def draw():
    
    global g
    
    # If the graph is completely calculated
    # (according to the number of iterations),
    # show shortest path between random nodes.
    path = []
    if g.update() == False:
        id1 = choice(g.index.keys())
        id2 = choice(g.index.keys())
        path = g.shortest_path(id1, id2)    
    
    # Draw the graph
    # and display the shortest path.
    g.draw(highlight=path)
    