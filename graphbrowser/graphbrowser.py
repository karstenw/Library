### CREDITS ##########################################################################################

__author__    = "Tom De Smedt"
__version__   = "alpha"
__copyright__ = "Copyright (c) 2007 Tom De Smedt"
__license__   = "Research purposes only"

### GRAPHBROWSER #####################################################################################

# A graph browser provides a way to browse through data interactively.
# A GraphBrowser needs to be inherited by another class that provides the data.
# Methods that need to be overridden:
# 1) has_node(node_id): returns True if the node_id is in the dataset
# 2) get_direct_links(node_id): a list of (weight, id) tuples directly connected to the node
# 3) get_links(node_id): a list of (weight, id, bindings) tuples of node id's that are
#    connected to the given node via the node id's in the bindings list.
# 4) get_node_descriptions(node_id): a list of descriptions for the given node id.
#    By default, attempts to return the WordNet interpretations of the id.

### GRAPHBROWSER #####################################################################################

class GraphBrowser:
    
    """ Interface between Graph and data.
    
    A graph browser adds hovering and clicking behaviour
    to a graph. This way you can switch from node to node.
    
    A browser has three methods which you need to override:
    has_node(), get_direct_links() and get_links().
    These provide the browser with linked nodes to display
    when you click on a node in the graph.
    
    You can then use the view() method to load a node to display,
    and draw() to redraw the browser to the canvas each frame.
    
    """
    
    def __init__(self):
        
        self.graph = None
        self.graph_distance = 1.85
        self.graph_iterations = 3000
        self.max = 20
        self.dx = 0
        self.dy = 0
        
        self.marquee = None
        self.marquee_speed = 3.0
        self.marquee_width = 200
    
    def has_node(self, node_id):
        
        """ Returns True if the network contains a node with the given id.

        This method needs to be overridden.

        """

        return False
    
    def get_direct_links(self, node_id):
        
        """ Retrieves id' of directly connected nodes.
        
        The return value is a list of 2-tuples,
        the first value being the weight of the connection,
        the second value the id of the linked node.
        
        This method needs to be overridden.
        
        """
        
        return []
        
    def get_links(self, node_id):
        
        """ Retrieves id's of related nodes.
        
        The return value is a list of 3-tuples,
        the first value being the weight of the connection,
        the second value the id of the linked node,
        the third value a list of id's linking the given
        node to the related node (i.e. links do not necessarily
        have to be directly connected but can have a distance of 2).
        
        This method needs to be overridden.
        
        """
        
        return []
        
    def get_node_descriptions(self, node_id):
        
        """ Get various descriptions for a node to display when hovering it.
        
        Returns a list of descriptions to display in
        the marquee box when hovering over the node.
        By default (when not overridden), this method returns
        the WordNet gloss descriptions for given node.
        
        """
        
        msg = []
        try:
            import en
            for i in range(len(en.noun.senses(node_id))):
                msg.append(node_id + " | " + en.noun.gloss(node_id, sense=i))       
        except:
            pass
        
        return msg
    
    def _reload(self, node_id, previous=None):
        
        """ Builds a graph around the given node id.
        
        Fetches direct and other links.
        Colorizes nodes according to their links.
        Adds a backlink to the previous node.
        
        """
        
        springgraph = _ctx.ximport("springgraph")
        
        g = springgraph.graph(iterations=self.graph_iterations, distance=self.graph_distance)
        g.hovered = self.node_hovered
        g.clicked = self.node_clicked
    
        # Root node with ROOT style.
        g.add_node(node_id, style=springgraph.STYLE_ROOT, root=True)
    
        # When the browser returns direct links for a node,
        # these have priority. Add them to the graph first and colorize them.
        # By default, all nodes have the LIGHT style.
        links = self.get_direct_links(node_id)
        for weight, linked_id in links:
            g.add_node(linked_id, style=springgraph.STYLE_LIGHT)
            g.add_edge(node_id, linked_id, weight=weight)
            if len(g.index) > self.max:
                break

        # Now get all the other links.
        links = self.get_links(node_id)
        for weight, linked_id, bindings in links:
            if linked_id not in g.index.keys():
                
                # The linked node is not yet in the graph, add it.
                # Its radius is based on a combination of weight and links.
                # It has the DEFAULT style.
                r = max(15, min(25, weight*5.0+len(bindings)/3))
                g.add_node(linked_id, radius=r)
                
                # Connect each intermediary node between
                # the root node and the linked node.
                # Intermediary nodes get the DARK style.    
                for bind_id in bindings:
                    if not bind_id in g.index:
                        g.add_node(bind_id, style=springgraph.STYLE_DARK)
                        g.add_edge(node_id, bind_id)
                    g.add_edge(bind_id, linked_id, weight=weight)
                if len(bindings) == 0:
                    g.add_edge(node_id, linked_id)
                    g.node(linked_id).style = springgraph.STYLE_LIGHT
            
            # Limit to a maximum amount of nodes onscreen.
            if len(g.index) > self.max:
                break
        
        # Nodes that have more than four children
        # get a different color, the IMPORTANT style.
        for n in g.nodes:
            count = len(n.links)
            n.r += count/2
            if n != g.nodes[0] and count > 5:
                n.style = springgraph.STYLE_IMPORTANT
        
        # Provide a backlink to the previous node,
        # the one displayed centrally when we clicked on this one.
        # This node gets the BACK style.
        if previous: 
            if not previous in g.index.keys():
                g.add_node(previous, style=springgraph.STYLE_BACK)
                g.add_edge(node_id, previous)
            else:
                g.index[previous].style=springgraph.STYLE_BACK
    
        self.graph = g
        return g
        
    def node_clicked(self, node):
        
        """ Callback from the browser's graph when a node is clicked.
        
        View the clicked node in the browser,
        unfolding the new graph from the position of
        the clicked node.
        
        """
        
        if not self.has_node(node.id):
            return
        if node == self.graph.nodes[0]:
            return
        
        d = self.graph.distance_from_center(node)
        self.dx = d.x
        self.dy = d.y
        p = self.graph.nodes[0].id
        if p == node.id:
            prev = None
        self._reload(node.id, previous=p)  

    def node_hovered(self, node):
        
        """ Display a marquee of node descriptions when hovering over a node.
        
        By default, these description are fed with WordNet gloss info
        returned from the GraphBrowser.get_node_descriptions() method.
        Uses the GraphMarquee's caching capabilities.
        
        """
        
        if (    self.marquee == None
             or self.marquee.id != node.id ):
            msg = self.get_node_descriptions(node.id)
            if len(msg) > 0:
                self.marquee = GraphMarquee(node.id, msg, speed=self.marquee_speed, w=self.marquee_width)
            else:
                self.marquee = None
    
        if self.marquee != None:
            x = node.x * node.graph.d + _ctx.fontsize()*2
            y = node.y * node.graph.d + _ctx.fontsize()*2.5
            self.marquee.draw(x, y)
    
    def view(self, node_id):
        
        if self.has_node(node_id):
            self._reload(node_id)
            
    def draw(self):
        
        if self.graph:
            self.graph.draw(self.dx, self.dy)
            self.dx *= 0.9
            self.dy *= 0.9
            
### GRAPHMARQUEE #####################################################################################   

class GraphMarquee:
    
    """ A box of rotating messages used when hovering over a node.
    
    The marquee can be fed with a queue of strings to display.
    These will rotate over time.
    Text to display is cached as a textpath for faster drawing.
    
    """
    
    def __init__(self, id, queue, speed=1.0, w=200):
        
        self.id = id
        self.queue = queue
        self.current = 0
        self.speed = speed
        self.intro = 20 / self.speed
        self.min_frames = 50
        self.frame = 0
        self.framecount = 0
        
        self.background = _ctx.color(0.0, 0.1, 0.15, 0.65)
        
        self._cache = None
        self._textwidth = w
        self._textheight = None
        
    def update(self):
        
        """ Rotates the queued messages to be displayed.
        """
        
        # Wait a certain amount of time
        # before the message pops up.
        if self.intro >= 0:
            self.intro -= 1
            return
        
        # Shows each message a number of frames,
        # based among the length of the text displayed.
        # Then rotate to the next message in queue.
        if len(self.queue) > 0:
            if self.frame == 0:
                if len(self.queue) > 1:
                    msg = self.queue[self.current]
                    self.framecount = len(msg) / self.speed
                    self.framecount = max(self.framecount, self.min_frames)
                else:
                    self.framecount = float("inf")
            self.frame += 1
            if self.frame > self.framecount:
                self.current += 1
                if self.current >= len(self.queue):
                    self.current = 0
                self.frame = 0
                
    def textpath(self):
        
        """ Returns a textpath of the current message in queue.
        """
        
        if self._cache == None \
        or self._cache[0] != self.current:
            # Cache the current textpath so it doesn't
            # need to be rebuilt every call.
            msg = self.queue[self.current]
            if len(self.queue) > 1:
                # Indicate current message (e.g. 5/13)
                msg += " ("+str(self.current+1)+"/"+str(len(self.queue))+")"
            self._textheight = _ctx.textheight(msg, width=self._textwidth)
            p = _ctx.textpath(msg, 0, 0, width=self._textwidth)
            self._cache = (self.current, p)
            
        i, p = self._cache
        return p
        
    def draw(self, x, y, scale=0.95):
        
        """ Draws a marquee box displaying messages.
        
        The background sets the color of the box,
        the text color is white. Displayed messages are rotated
        automatically.
        
        """ 
        
        self.update()
        
        if len(self.queue) > 0 \
        and self.intro <= 0:
            fs = _ctx.fontsize()
            p = self.textpath()
            _ctx.fill(self.background)
            _ctx.rect(x-fs, y-fs*1.75, 
                      self._textwidth+fs,
                      self._textheight+fs*1.5, roundness=0.2)
            # Fade in and fade out the current message.
            if self.frame < 10:
                a = self.frame * 0.2
            elif self.framecount-self.frame < 10:
                a = (self.framecount-self.frame) * 0.2
            else:
                a = 1.0
            _ctx.fill(1,1,1, a)
            _ctx.translate(x, y)
            _ctx.scale(scale)
            _ctx.drawpath(p)