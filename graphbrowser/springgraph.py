### CREDITS ##########################################################################################

# Copyright (c) 2007 Tom De Smedt.
# See LICENSE.txt for details.

__author__    = "Tom De Smedt"
__version__   = "alpha"
__copyright__ = "Copyright (c) 2007 Tom De Smedt"
__license__   = "Research purposes only"

### SPRINGGRAPH ######################################################################################

# The NodeBox Springgraph library provides tools to implement a fast graph in animation.
# You can load it with connected nodes and display them as a network of data,
# or find the shortest path between two nodes using the Dijkstra algorithm.

# The Springgraph is extended in Graphbrowser which links user interaction to datasets
# and the graphing math.

######################################################################################################

import pprint

from nodebox.graphics import Point, RGB
from nodebox.util import random,makeunicode
from math import sqrt, log
from math import degrees, atan2

STYLE_DEFAULT   = "default"
STYLE_HIGHLIGHT = "highlight"
STYLE_ROOT      = "root"
STYLE_LIGHT     = "light"
STYLE_DARK      = "dark"
STYLE_BACK      = "back"
STYLE_IMPORTANT = "important"
STYLE_MARKED    = "marked"
STYLE_BLUE      = "blue"

#### GRAPHNODE #######################################################################################

class GraphNode:
    
    def __init__(self, graph, id="", radius=8, style=STYLE_DEFAULT):
        
        """ A node with a unique id in the graph.
        
        Its position is set once a layout is iterated.
        The node's radius and style define how it looks onscreen.
        
        """
        
        self.graph = graph
        self.id = id
        self.links = []
        self.weight = None
        self.x = 0
        self.y = 0
        self.force = Point(0, 0)
        self.r = radius
        self.style = style
        
    def _edges(self):
        
        """ Returns a list of id's this node is connected to.
        """
        
        all = []
        for e in self.graph.edges:
            if self in (e.node1, e.node2):
                all.append(e)
            
        return all

    edges = property(_edges)

##### GRAPHEDGE ######################################################################################

class GraphEdge:
    
    def __init__(self, node1, node2, weight=1.0, label=""):
        
        """ A connection between two nodes in the graph.
        """
        
        self.node1 = node1
        self.node2 = node2
        self.label = label
        self.weight = weight

#### GRAPH ###########################################################################################

class Graph:
    
    def __init__(self, iterations=500, distance=1.0):
        
        self.index = {}
        self.nodes = []
        self.edges = []
        self.root = None
        
        self.layout = GraphSpringLayout(self, iterations)
        self.iteration = 0
        self.d = GraphNode(None).r * 2 * distance
        
        self.pathfinder = GraphShortestPath()
        
        self.styles = GraphStyles()
        self.styles.append(GraphStyle(STYLE_DEFAULT))
        self.alpha = 0
        
        self.pressed = None
        self.dragged = None
        self.clicked = None
        self.hovered = None
        
    def add_node(self, id, radius=15, style=STYLE_DEFAULT, root=False):
        
        """ Adds a node with given id to the graph.
        """
        
        if id in self.index:
            return self.index[id]
        
        n = GraphNode(self, id, radius, style)
        self.index[n.id] = n
        self.nodes.append(n)
        if root: 
            self.root = n
            
        return n
        
    def add_edge(self, id1, id2, weight=1.0, label=""):
        
        """ Creates a link between the nodes with given id's.
        """
        
        n1 = self.index[id1]
        n2 = self.index[id2]
        
        if n1 in n2.links and n2 in n1.links:
            return self.edge(id1, id2)
                    
        n1.links.append(n2)
        n2.links.append(n1)
        e = GraphEdge(n1, n2, weight, label)
        self.edges.append(e)
        
        return e
        
    def remove_node(self, id):
        
        """ Removes the node with the given id and any links to other nodes.
        """
        
        if self.index.has_key:
            n = self.index[id]
            self.nodes.remove(n)
            del self.index[id]
            
            # Remove all edges involving id and all links to it.
            for e in self.edges:
                if n in (e.node1, e.node2):
                    if n in e.node1.links: 
                        e.node1.links.remove(n)
                    if n in e.node2.links: 
                        e.node2.links.remove(n)
                    self.edges.remove(e)

    def node(self, id):
        
        """ Returns the node in the graph associated with the given id.
        """
        
        if id in self.index:
            return self.index[id]
        else:
            return None
    
    def edge(self, id1, id2):
        
        """ Returns the edge between the nodes with given id1 and id2.
        """
        
        for e in self.edges:
            if e.node1.id in (id1, id2) and \
               e.node2.id in (id1, id2):
                return e
    
        return None
    
    def update(self, iterations=10):
        
        """ Iterates the graph layout.
        """    

        # The graph fades in when initially constructed.
        self.alpha += 0.05
        self.alpha = min(self.alpha, 1.0)

        # Iterates over the graph's layout.
        # Each step the graph's bounds are recalculated
        # and a number of iterations are processed,
        # more and more as the layout progresses.
        if self.iteration == 0:
            self.layout.prepare()
            self.layout.calculate_bounds()
            self.iteration += 1
        elif self.iteration == 1:
            self.iteration += 1
        elif (    self.iteration < self.layout.iterations
              and self.iteration > 1):
            n = int( min(iterations, self.iteration / 10 + 1) )
            for i in range(n): 
                self.layout.iterate()
            self.layout.calculate_bounds()
            self.iteration += n
        else:
            return False
    
        return True
        
    def solve(self):
        
        """ Iterates the graph layout until done.
        """
        
        done = False
        while not done:
            done = not self.update()
    
    def center(self):
        
        """ The absolute center of the graph on the canvas.
        """
        
        try:
            x = _ctx.WIDTH - self.max.x*self.d - self.min.x*self.d
            y = _ctx.HEIGHT - self.max.y*self.d - self.min.y*self.d
            x /= 2
            y /= 2
        except:
            x = _ctx.WIDTH/2
            y = _ctx.HEIGHT/2
            
        return Point(x, y)
        
    def distance_from_center(self, node):
        
        """ Returns the absolute distance from the canvas center for given node.
        """
        
        c = self.center()
        x = c.x + node.x * self.d - _ctx.WIDTH/2
        y = c.y + node.y * self.d - _ctx.HEIGHT/2
        
        return Point(x, y)
    
    def draw(self, dx=0, dy=0, highlight=[], clusters=True):
        
        """ Layouts the graph incrementally.
        
        The graph is drawn at the center of the canvas,
        with a deviation of dx and dy.
        The highlight parameter specifies a path of connected nodes. 
        The path will be colored according to the "highlight" style.
        Clicking and dragging events are monitored.
        
        """
        
        self.update()

        # Draw the graph background.
        s = self.styles.default
        s.draw.background(s)

        # Center the graph on the canvas.
        c = self.center()
        _ctx.translate(c.x+dx, c.y+dy)
 
 
        
        if clusters:
            for n in self.strongest_nodes()[:3]:
                try: s = self.styles[n.style]
                except: s = self.styles.default
                s.draw.cluster(s, n, self.alpha)        



        # Draws the graph's edges as a single Bezier path for speed.
        # The color of the default style's stroke is used,
        _ctx.nofill()
        _ctx.nostroke()
        if s.stroke: 
            _ctx.stroke(s.stroke.r, s.stroke.g, s.stroke.g, s.stroke.a*self.alpha*0.65)
        _ctx.strokewidth(s.strokewidth)
        _ctx.autoclosepath(False)
        _ctx.beginpath(0, 0)
        for e in self.edges:
            try:  s = self.styles[e.node1.style]
            except: s = self.styles.default
            s.draw.edge(s, e.node1.x*self.d, e.node1.y*self.d,
                           e.node2.x*self.d, e.node2.y*self.d, e)
        _ctx.endpath()
        
        for e in self.edges:
            try:  s = self.styles[e.node1.style]
            except: s = self.styles.default
            s.draw.edge_label(s, e, self.alpha)
                
        # Highlights a given path between nodes.
        if len(highlight) > 1:
            try:  s = self.styles.highlight
            except: s = self.styles.default
            _ctx.nofill()
            _ctx.stroke(s.stroke)
            if s != self.styles.default:
                _ctx.strokewidth(s.strokewidth)
            else:
                _ctx.strokewidth(s.strokewidth*2)
            first = True
            for id in highlight:
                n = self.index[id]
                if first:
                    _ctx.beginpath(n.x*self.d, n.y*self.d)
                    first = False
                else:
                    _ctx.lineto(n.x*self.d, n.y*self.d)
            _ctx.endpath()

        # Draws each node in the graph.
        # Applies individual style to each node
        # or the default style when no style is specified.        
        for n in self.nodes:
            try:  s = self.styles[n.style]
            except: s = self.styles.default
            s.draw.node(s, n, self.alpha)
        
        # Draws node id's as labels on each node.
        for n in self.nodes:
            try:  s = self.styles[n.style]
            except: s = self.styles.default
            s.draw.node_label(s, n, self.alpha)
        
        # Events for clicked and dragged nodes.
        # Nodes will resist being dragged by attraction and repulsion,
        # put the event listener on top to get more direct feedback.
        self.events()
    
    def mouse_inside(self, node):
        
        """ Checks whether the mouse hovers the given node.
        
        This is based on the absolute position of the node,
        which is its position * d + center
        
        """
        
        c = self.center()
        if  abs(c.x+node.x * self.d - _ctx._ns["MOUSEX"]) < node.r \
        and abs(c.y+node.y * self.d - _ctx._ns["MOUSEY"]) < node.r:    
            return True
        else:
            return False    
    
    def drag(self, node):
        
        """ Drag given node to mouse location.
        
        The node will resist being dragged by attractive and repulsive forces.
        A dashed line indicates the drag vector.
        
        """
        
        c = self.center()
        dx = _ctx._ns["MOUSEX"] - c.x
        dy = _ctx._ns["MOUSEY"] - c.y

        s = self.styles.default
        _ctx.nofill()
        _ctx.nostroke()
        if s.stroke: 
            _ctx.stroke(s.stroke.r, s.stroke.g, s.stroke.g, 0.75)
            _ctx.strokewidth(s.strokewidth)
        p = _ctx.line(node.x*self.d, node.y*self.d, dx, dy, draw=False)
        p._nsBezierPath.setLineDash_count_phase_([2,4], 2, 50)
        _ctx.drawpath(p)
        r = GraphNode(None).r * 0.75
        _ctx.oval(dx-r/2, dy-r/2, r, r)
        
        node.x = dx/self.d
        node.y = dy/self.d
    
    def events(self):
        
        """ Interact with the graph by clicking or dragging nodes.
        
        Clicking a node fires the callback function Graph.clicked.
        It takes one parameter (which is the node clicked).
        
        """
        
        if _ctx._ns["mousedown"]:
            
            # When not pressing or dragging a node,
            # check each node to see if it is being pressed.
            if not self.pressed \
            and not self.dragged:
                for n in self.nodes:
                    if self.mouse_inside(n):
                        self.pressed = n
                        break
            
            # When pressing a node,
            # check to see if the mouse moves beyond the node radius
            # meaning the node is being dragged.
            elif self.pressed \
            and not self.mouse_inside(self.pressed):
                self.dragged = self.pressed
                self.pressed = None
            
            # Drag the node.
            elif self.dragged:
                self.drag(self.dragged)
                self.iteration = min(100, max(2, self.layout.iterations-100))
        
        # Mouse is pressed and released inside a node,
        # fire the node click behavior.
        elif self.pressed \
        and self.mouse_inside(self.pressed):
            if self.clicked: 
                self.clicked(self.pressed)
                self.iteration = 2
            self.pressed = None
        
        # Nothing is being pressed, clicked or dragged.
        else:
            self.pressed = None
            self.dragged = None
            
            # Is the mouse hovering over a node?
            for n in self.nodes:
                if self.mouse_inside(n):
                    if self.hovered: self.hovered(n)
                    break
                
    def distance_map(self):
        
        """ Calculates distance between connected nodes.
        
        The return value is a dictionary indexed by node id's.
        Each value is a dictionary of connected node id's
        linked to the distance between both nodes.
        
        """
        
        # If we haven't done any new iterations,
        # the distances between nodes haven't changed
        # and we can use a cached distance map.
        try:
            i, map = self._v
            if i == self.iteration: 
                return map
        except:
            pass
        
        v = {}
        for n1 in self.nodes:
            vn1 = {}
            for n2 in n1.links:
                dx = n2.x - n1.x
                dy = n2.y - n1.y
                d = sqrt(abs(dx) + abs(dy))
                vn1[n2.id] = d
            v[n1.id] = vn1
        
        self._v = self.iteration, v
        return v
    
    def shortest_path(self, id1, id2):
        
        """ Returns a list of node id's connecting the two nodes.
        """
        
        v = self.distance_map()
        try:
            return self.pathfinder.find(v, id1, id2)
        except:
            return []
            
    def strongest_nodes(self, treshold=0.0):
        
        nodes = []
        for i,n in enumerate(self.nodes):
            if n.weight and n.weight > treshold:
                nodes.append( (n.weight, i) )
        # nodes = [(n.weight, n) for n in self.nodes if n.weight and n.weight > treshold]
        
        try:
            nodes.sort()
        except TypeError:
            #import pdb
            #pdb.set_trace()
            pprint.pprint( nodes )
            print()
        nodes.reverse()
        # nodes = [n for s, n in nodes]
        result = []
        for node in nodes:
            w,i = node
            result.append( self.nodes[i] )
        return result

##### GRAPHSPRINGLAYOUT ##############################################################################

class GraphSpringLayout:
    
    """ Graph layout based on attractive and repulsive forces.
    
    Taken from a Javascript Spring Graph script:
    http://snipplr.com/view/1950/graph-javascript-framework-version-001/
    
    Calculates node positions when iterate() is called.
    The more iterations the better the layout,
    usually GraphSpringLayout.iterations is a good maximum of iterations.
    
    """
    
    def __init__(self, graph, iterations=500):
        
        self.graph = graph
        self.iterations = iterations
        self.max_repulsive_force_distance = 6
        self.k = 2
        self.c = 0.01
        self.max_vertex_movement = 0.5
    
    def prepare(self):
        
        for n in self.graph.nodes:
            n.x = 0
            n.y = 0
            n.force = Point(0,0)
            
        for e in self.graph.edges:
            e.weight = max(e.weight, 1)
        
    def calculate_bounds(self):
        
        min = Point(float("inf"), float("inf"))
        max = Point(float("-inf"), float("-inf"))
        
        for n in self.graph.nodes:
            if (n.x > max.x): max.x = n.x
            if (n.y > max.y): max.y = n.y
            if (n.x < min.x): min.x = n.x
            if (n.y < min.y): min.y = n.y
            
        self.graph.min = min
        self.graph.max = max
        
    def iterate(self):
        
        # Forces on nodes due to node-node repulsions
        for i in range(len(self.graph.nodes)):
            n1 = self.graph.nodes[i]
            for j in range(i+1, len(self.graph.nodes)):
                n2 = self.graph.nodes[j]
                self.repulse(n1, n2)
        
        # Forces on nodes due to edge attractions
        for e in self.graph.edges:
            self.attract(e)
            
        # Move by given force
        for n in self.graph.nodes:
            dx = self.c * n.force.x
            dy = self.c * n.force.y
            max = self.max_vertex_movement
            if (dx > max): dx = max
            if (dy > max): dy = max
            if (dx < -max): dx = -max
            if (dy < -max): dy = -max
            n.x += dx
            n.y += dy
            n.force.x = 0
            n.force.y = 0
    
    def repulse(self, n1, n2):
        
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        d2 = dx * dx + dy * dy
        
        if d2 < 0.01:
            dx = 0.1 * random() + 0.1
            dy = 0.1 * random() + 0.1
            d2 = dx * dx + dy * dy
        
        d = sqrt(d2)
        if d < self.max_repulsive_force_distance:
            f = self.k * self.k / d
            n2.force.x += f * dx / d
            n2.force.y += f * dy / d
            n1.force.x -= f * dx / d
            n1.force.y -= f * dy / d
        
    def attract(self, edge):
        
        (n1, n2) = (edge.node1, edge.node2)
        
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        d2 = dx * dx + dy * dy
        
        if d2 < 0.01:
            dx = 0.1 * random() + 0.1
            dy = 0.1 * random() + 0.1
            d2 = dx * dx + dy * dy
            
        d = sqrt(d2)
        if d > self.max_repulsive_force_distance:
            d = self.max_repulsive_force_distance
            d2 = d * d
        
        f = (d2 - self.k * self.k) / self.k
        f *= edge.weight * 0.5 + 1
        
        n2.force.x -= f * dx / d
        n2.force.y -= f * dy / d
        n1.force.x += f * dx / d
        n1.force.y += f * dy / d

#### GRAPHSHORTESTPATH ###############################################################################

class GraphShortestPath:
        
    def find(self, G, start, end):

        """ Dijkstra shortest path algorithm.
        
        From the Python Cookbook, Connelly Barnes:
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466
        
        Raises an IndexError when trying to find a path
        between nodes on different unconnected graphs.
        
        """
        
        import heapq
        from sets import Set
        
        # Flatten linked list of form [0,[1,[2,[]]]]
        def flatten(L):       
            while len(L) > 0:
                yield L[0]
                L = L[1]

        q = [(0, start, ())]  # Heap of (cost, path_head, path_rest).
        visited = Set()       # Visited vertices.
        while True:
            (cost, v1, path) = heapq.heappop(q)
            if v1 not in visited:
                visited.add(v1)
            if v1 == end:
                return list(flatten(path))[::-1] + [v1]
            path = (v1, path)
            for (v2, cost2) in G[v1].items():
                if v2 not in visited:
                    heapq.heappush(q, (cost + cost2, v2, path))

#### GRAPHSTYLE ######################################################################################

class GraphStyles(dict):
    
    def append(self, style):
        
        self[style.name] = style
    
    def __getattr__(self, a):
        
        """ Keys in the dictionaries are accessible as attributes.
        """ 
        
        if a in self: 
            return self[a]
            
        raise AttributeError( "'GraphStyles' object has no attribute '"+a+"'" )
        
    def __setattr__(self, a, v):
        
        """ Setting an attribute is like setting it in all of the contained styles.
        """
        
        if a in GraphStyle(None).__dict__:
            for style in self.values():
                style.__dict__[a] = v
                
        else:
            raise AttributeError( "'GraphStyle' object has no attribute '"+a+"'" )

#### GRAPHSTYLE ######################################################################################
        
class GraphStyle:
    
    def __init__(self, name):
        
        """ Styles a node in the graph.
        
        The default style is used for edges.
        When text is set to None, no id label is displayed.
        
        """

        self.name = name
        self.background = _ctx.color(0.18, 0.23, 0.28)
        self.cluster = _ctx.color(0.0, 0.0, 0.0, 0.075)
        self.fill = _ctx.color(0.0, 0.0, 0.0, 0.10)
        self.stroke = _ctx.color(0.8, 0.8, 0.8, 0.75)
        self.strokewidth = 0.5
        self.text = _ctx.color(1.0, 1.0, 1.0, 0.85)
        self.font = "Verdana"
        self.fontsize = 10
        self.textwidth = 100
        
        try: 
            global colors
            colors = None
            colors = _ctx.ximport("colors")
        except: 
            pass
    
        self.draw = GraphDraw()

#### GRAPHDRAW ####################################################################################### 

# The draw methods are actually just a bunch of functions,
# so another function can easily be assigned.
# Just call GraphStyle.draw.method(GraphStyle, parameters)
# instead of GraphStyle.draw.method(parameters). 

class GraphDraw:
    
    def __init__(self):
        
        self.node       = draw_node
        self.edge       = draw_edge
        self.node_label = draw_node_label
        self.edge_label = draw_edge_label
        self.background = draw_background
        self.cluster    = draw_cluster        

#--- DRAW_BACKGROUND ---------------------------------------------------------------------------------

def draw_background(style):

    """ Override this method to get a different background.
    """

    if style.background == None:
        _ctx.background(None)

    try:
        global colors
        clr = colors.color(style.background).darker(0.2)
        p = _ctx.rect(0, 0, _ctx.WIDTH, _ctx.HEIGHT, draw=False)
        colors.gradientfill(p, clr, clr.lighter(0.35))
        colors.shadow(dx=0, dy=0, blur=2, alpha=0.935, clr=style.background)
    except:
        _ctx.background(style.background)  

#--- DRAW_NODE ---------------------------------------------------------------------------------------

def draw_cluster(style, node, alpha=1.0):
    
    r = node.weight * GraphNode(None).r * 10
    _ctx.nostroke()
    _ctx.fill(style.cluster.r, style.cluster.g, style.cluster.b, style.cluster.a*alpha)
    _ctx.oval(node.x * node.graph.d - r*0.5, 
              node.y * node.graph.d - r*0.5, r, r)      

#--- DRAW_NODE ---------------------------------------------------------------------------------------

def draw_node(style, node, alpha=1.0):
    
    """ Override this method to get a different shape of node.
    """
    
    try: colors.shadow(dx=5, dy=10, blur=10, alpha=1.0, clr=style.background)
    except: pass
    
    _ctx.nofill()
    _ctx.nostroke()
    if style.fill:
        _ctx.fill(style.fill.r, style.fill.g, style.fill.b, style.fill.a*alpha)
    if style.stroke: 
        _ctx.strokewidth(style.strokewidth)
        _ctx.stroke(style.stroke.r, style.stroke.g, style.stroke.g, style.stroke.a*alpha*3)
    r = node.r
    _ctx.oval(node.x * node.graph.d - r*0.5, 
              node.y * node.graph.d - r*0.5, r, r)        

#--- DRAW_NODE_LABEL --------------------------------------------------------------------------------

def draw_node_label(style, node, alpha=1.0):

    """ Override this method to get a different node label.
    """
    
    if style.text:

        _ctx.nostroke()
        _ctx.fill(style.text.r, style.text.g, style.text.b, style.text.a*alpha)
        _ctx.lineheight(1)    
        _ctx.font(style.font)
        _ctx.fontsize(style.fontsize)

        # Cache an outlined label text and translate it.
        # This enhances the speed and avoids wiggling text.
        try: p = node._textpath
        except: 
            # txt = unicode(node.id)
            txt = str(node.id)
            #try:
            #    txt = txt.decode("utf-8")
            #except:
            #    pass
            root = node.graph.nodes[0].id
            # Abbreviation.
            #if txt != root and txt[-len(root):] == root: 
            #    txt = txt[:len(txt)-len(root)]+root[0]+"."
            node._textpath = _ctx.textpath(txt, _ctx.textwidth(" "), 0, width=style.textwidth)
            p = node._textpath
        
        try: colors.shadow(dx=2, dy=4, blur=5, alpha=1.0, clr=style.background)
        except: pass
        
        _ctx.push()
        _ctx.translate(node.x * node.graph.d, 
                       node.y * node.graph.d)
        _ctx.scale(alpha)
        _ctx.drawpath(p)
        _ctx.pop()

#--- DRAW_EDGE ---------------------------------------------------------------------------------------

def draw_edge(style, x0, y0, x1, y1, edge):
    
    """ Override this method to get a different edge connection.
    """
    
    _ctx.moveto(x0, y0)
    if edge.node2.style == STYLE_BACK:
        dy = y0-y1
        _ctx.curveto(x0, y0-dy, x1, y1, x1, y1)
    else:
        _ctx.lineto(x1, y1)

#--- DRAW_EDGE_LABEL ---------------------------------------------------------------------------------

def draw_edge_label(style, edge, alpha=1.0):

    """ Override this method to get a different edge label.
    """
    
    if style.text and edge.label != "":
        
        _ctx.nostroke()
        _ctx.fill(style.text.r, style.text.g, style.text.g, style.text.a*alpha*0.75)
        _ctx.lineheight(1)    
        _ctx.font(style.font)
        _ctx.fontsize(style.fontsize*0.75)
        
        # Cache an outlined label text and translate it.
        # This enhances the speed and avoids wiggling text.
        try: p = edge._textpath
        except: 
            txt = unicode(edge.label)
            try: txt = txt.decode("utf-8").upper()
            except:
                pass
            edge._textpath = _ctx.textpath(txt, _ctx.textwidth(" "), 0, width=style.textwidth)
            p = edge._textpath
        
        # Position the label centrally along the edge line.
        a  = degrees( atan2(edge.node2.y-edge.node1.y, edge.node2.x-edge.node1.x) )
        d  = sqrt(pow(edge.node2.x-edge.node1.x, 2) + pow(edge.node2.y-edge.node1.y, 2))
        d *= edge.node1.graph.d
        d  = abs(d-_ctx.textwidth(edge.label)) * 0.5
        
        _ctx.push()
        _ctx.transform(CORNER)
        _ctx.translate(edge.node1.x * edge.node1.graph.d, 
                       edge.node1.y * edge.node1.graph.d)
        _ctx.rotate(-a)
        _ctx.translate(d, style.fontsize*1.0)
        _ctx.scale(alpha)
        
        # Flip labels on the left hand side so they are legible.
        if 90 < a%360 < 270:
            _ctx.translate(_ctx.textwidth(edge.label), -style.fontsize*2.0)
            _ctx.transform(CENTER)
            _ctx.rotate(180)
            _ctx.transform(CORNER)
        
        _ctx.drawpath(p)
        _ctx.pop()        

#### COMMANDS ########################################################################################

def graph(iterations=500, distance=1.0):
    
    """ Returns an empty graph with some predefined styles.
    """

    _ctx.colormode(RGB)
    g = Graph(iterations, distance)
    
    g.styles.append(graph_style(STYLE_LIGHT    , fill   = _ctx.color(0.0, 0.0, 0.0, 0.20)))
    g.styles.append(graph_style(STYLE_DARK     , fill   = _ctx.color(0.3, 0.5, 0.7, 0.75)))
    g.styles.append(graph_style(STYLE_BACK     , fill   = _ctx.color(0.5, 0.8, 0.0, 0.50)))
    g.styles.append(graph_style(STYLE_BLUE     , fill   = _ctx.color(0.1, 0.1, 0.9, 0.50)))
    g.styles.append(graph_style(STYLE_IMPORTANT, fill   = _ctx.color(0.3, 0.6, 0.8, 0.75)))
    g.styles.append(graph_style(STYLE_HIGHLIGHT, stroke = _ctx.color(1.0, 0.0, 0.5), strokewidth=1.5))
    g.styles.append(graph_style(STYLE_MARKED))
    g.styles.append(graph_style(STYLE_ROOT     , text   = _ctx.color(1.0, 0.0, 0.4, 1.00), 
                                                 stroke = _ctx.color(0.8, 0.8, 0.8, 0.60),
                                                 strokewidth=1.5, 
                                                 fontsize=16, 
                                                 textwidth=150))

    # Important nodes get a double stroke.
    def draw_important_node(style, node, alpha=1.0):
        GraphStyle(None).draw.node(style, node, alpha)
        r = node.r * 1.4
        _ctx.nofill()
        _ctx.oval(node.x * node.graph.d - r*0.5, 
                  node.y * node.graph.d - r*0.5, r, r)  

    # Marked nodes have an inner dot.
    def draw_marked_node(style, node, alpha=1.0):
        GraphStyle(None).draw.node(style, node, alpha)
        r = node.r * 0.3
        _ctx.fill(style.stroke)
        _ctx.oval(node.x * node.graph.d - r*0.5, 
                  node.y * node.graph.d - r*0.5, r, r)
    
    g.styles.important.draw.node = draw_important_node
    g.styles.marked.draw.node = draw_marked_node            

    return g
    
def graph_style(
    name,
    background  = None, 
    fill        = None, 
    stroke      = None, 
    strokewidth = None, 
    text        = "", 
    font        = None, 
    fontsize    = None, 
    textwidth   = None):
    
    """ Returns a new style template for graph elements.
    """
    
    s = GraphStyle(name)
    if background  : s.background = background
    if fill        : s.fill = fill
    if stroke      : s.stroke = stroke
    if strokewidth : s.strokewidth = strokewidth
    if text != ""  : s.text = text
    if font        : s.font = font
    if fontsize    : s.fontsize = fontsize
    if textwidth   : s.textwidth = textwidth
    
    return s

style = graphstyle = graph_style

"""    
g = graph(distance=3)
g.add_node("nodebox")
g.add_node("gravital")
g.add_node("coreimage")
g.add_node("bezier")
g.add_edge("nodebox", "gravital")
g.add_edge("nodebox", "coreimage", label="part_of")
g.add_edge("nodebox", "bezier", label="part_of")

size(500,500)
speed(10)
def draw():
    g.draw()
"""



def centrality(g, normalized=True):

    """ Brandes betweenness centrality.
    
    Calculates the betweenness centrality for nodes in the graph,
    based on the number of shortests paths that pass through each node.
    
    The algorithm is Brandes' betweenness centrality,
    from NetworkX, Aric Hagberg, Dan Schult and Pieter Swart,
    based on Dijkstra's algorithm for shortest paths modified from Eppstein.
    
    """

    import heapq 
    G = g.index.keys()
    betweenness = dict.fromkeys(G, 0.0) # b[v]=0 for v in G
    for s in G: 
        S = [] 
        P = {} 
        for v in G: 
            P[v] = [] 
        sigma = dict.fromkeys(G, 0) # sigma[v]=0 for v in G 
        D = {} 
        sigma[s] = 1
        seen = { s: 0 }  
        Q = [] # use Q as heap with (distance,node id) tuples 
        heapq.heappush(Q, (0, s, s)) 
        while Q:    
            (dist, pred, v) = heapq.heappop(Q) 
            if v in D: 
                continue # already searched this node. 
            sigma[v] = sigma[v] + sigma[pred] # count paths 
            S.append(v) 
            D[v] = seen[v] 
            for w in g.index[v].links:
                w = w.id
                
                vw_dist = D[v] + 1/g.distance_map()[w][v]*10
                vw_dist = D[v] #- 1/g.distance_map()[w][v]
                
                if w not in D and (w not in seen or vw_dist < seen[w]): 
                    seen[w] = vw_dist 
                    heapq.heappush(Q, (vw_dist, v, w)) 
                    P[w] = [v] 
                elif vw_dist == seen[w]: # handle equal paths 
                    sigma[w] = sigma[w] + sigma[v] 
                    P[w].append(v)
                    
        delta = dict.fromkeys(G,0)  
        while S: 
            w = S.pop() 
            for v in P[w]: 
                delta[v] = delta[v] + (float(sigma[v]) / float(sigma[w])) * (1.0 + delta[w]) 
                if w != s: 
                    betweenness[w] = betweenness[w] + delta[w]

        if normalized:
            s = sum(betweenness.values())
            if s == 0: s = 1
            sorted = [(w/s, id) for id, w in betweenness.items()]
            sorted.sort()
            sorted.reverse()
            sorted = [(id, w) for w, id in sorted]
            for id, w in sorted:
                g.index[id].weight = w+1
                print( w )
            return sorted
                    
        return betweenness

