# A graph that browses through the WordNet dictionary.

springgraph = ximport("springgraph")
#reload(springgraph)

graphbrowser = ximport("graphbrowser")
#reload(graphbrowser)

import linguistics
import pattern
import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = en.wordnet

# pattern = ximport("pattern")
# en = pattern.text.en

from random import shuffle

import pdb
import pprint
pp=pprint.pprint
# pdb.set_trace()

allnouns = list(wordnet.NOUNS())


class WordNetBrowser(graphbrowser.GraphBrowser):
    
    """ Browse WordNet in a graph.
    
    WordNet provides extensive information on lexical relationships,
    and coupled to the gloss of each word displayed as a marquee popup 
    you get tons of factual and historical data as well.
    
    Getting data from WordNet is pretty straightforward
    but a lot of the code here is complicated to make
    the parts/specific branches in the graph clickable.
    
    """
    
    def __init__(self):
        
        # Keep the word sense as a state parameter.
        pdb.set_trace()
        graphbrowser.GraphBrowser.__init__(self)
        self.sense = 0
        self.sense_count = 0
        self.sense_mousedown = None

    def has_node(self, node_id):

        # Accept clicks on the "parts" and "specific" branches
        # (unless it is the root node being clicked).
        # In this case get_branch_details() is called.
        if node_id in ("parts ", "specific "):
            if node_id != self.graph.nodes[0].id:
                return True
        if node_id.lower() in allnouns:
            return True
        if node_id in ("parts ", "specific "):
            return True
        return False


    def get_direct_links(self, node_id, top=6):
        
        if node_id in ["parts ", "specific "]: 
            return []
        
        # If there would be 4 senses,
        # and each of it a list of words,
        # take the first word from each sense list,
        # then take the second word etc. up to top.
        children = []
        
        # senses = en.noun.senses(node_id)
        senses = wordnet.synsets( node_id ).senses
        for i in range( 2 ):
            for sense in senses:
                if (    len(sense) > i 
                    and sense[i] != node_id 
                    and sense[i] not in children ):
                    children.append(sense[i])
                    
        children = [(5,id) for id in children]
        return children[:top]

    def get_links(self, node_id):
        
        if node_id == "specific ":
            return self.get_branch_details("hyponym")
        if node_id == "parts ":
            return self.get_branch_details("holonym")
        
        children = []
        lexname = en.noun.lexname(node_id)
        if lexname != "":
            children.append( (1, lexname, ["category "]) )
        
        branches = [
            (6, en.noun.holonym  , "parts "),
            (2, en.noun.meronym  , "part of "),
            (2, en.noun.antonym  , "opposite "),
            (3, en.noun.hypernym , "generic "),
            (2, en.verb.senses   , "action "),
            (6, en.noun.hyponym  , "specific "),
        ]
        # For each of the branches, get all the words from WordNet.
        # Exclude long words.
        # Shuffle the list and then take the top.
        for top, f, label in branches:
            branch = []
            # The lookup for verb senses might not work with a noun,
            # then we get idiotic error stuff like:
            # KeyError: "'florenz ziegfeld' is not in the 'verb' database"
            try:
                for n in f(node_id, sense=self.sense):
                    if  n[0] != node_id \
                    and n[0] not in branch \
                    and len(n[0]) < 20:
                        branch.append( (10, n[0], [label]) )
            except: pass
            #shuffle(branch)
            children.extend(branch[:top])
            
        return children

    def get_branch_details(self, branch):
        
        """ Fetches data when clicked on the parts/specific branches.
        """
        
        root = self.graph.nodes[0].id.lower()
        # f = getattr(en.noun, branch)
        # This is more readable:
        if branch == "hyponym": f = en.noun.hyponym
        if branch == "holonym": f = en.noun.holonym
        
        unique = []
        for n in f(root, sense=self.sense):
            if n[0] not in unique: unique.append(n[0])
        shuffle(unique)
        
        children = []
        i = 0
        for n in unique:
            # Organise connected nodes in branches,
            # each branch carries 4 nodes.
            # Nodes that have the root id in their own id,
            # form a branch on their own.
            binding = " "
            if n.find(root) < 0:
                binding = (i+4)/4*"  "
                i += 1
            children.append( (10, n, [binding]) )
            
        return children
        
    def _reload(self, node_id, previous=None):
        
        # If the previously viewed node was
        # the details of the parts/specific branch,
        # it will be named something like "specific [root]s".
        # Strip the [root] part.
        if previous != None:
            if previous.find("specific ") == 0:
                if previous.find(node_id) > 0:
                    previous = "specific "
                else:
                    previous = self.graph.nodes[-1].id
                self.max += 10
            if previous.find(" parts") > 0:
                if previous.find(node_id) > 0:
                    previous = "parts "
                else:
                    previous = self.graph.nodes[-1].id
        
        # If a new node is loaded, reset the current sense.
        if (    self.graph
            and node_id != self.graph.root.id
            and node_id not in ["parts ", "specific "]
            and previous not in ["parts ", "specific "] ):
            self.sense = 0
        
        graphbrowser.GraphBrowser._reload(self, node_id, previous)

        # Get the number of senses of this node.
        # Find the node in the graph matching that sense.
        # It's one of the nodes directly connected to the root.
        # Mark it with an appropriate style.
        try:
            senses = en.noun.senses(node_id)
            self.sense_count = len(senses)
            for word in senses[self.sense]:
                if word != self.graph.root.id:
                    node = self.graph.node(word)
                    if node:
                        node.style = springgraph.STYLE_MARKED
        except:
            self.sense_count = 0

        # If the current viewed node is
        # the details of the parts/specific branch,
        # format the root name like "specific [root]s"
        # instead of just "specific".
        root = self.graph.root      
        if root.id == "specific ": 
            root.id += en.noun.plural(previous)
            self.max -= 10
        if root.id == "parts ": 
            root.id = previous+" parts"

    def draw(self):
        
        """ Additional drawing and events for sense selection buttons.
        """
        
        graphbrowser.GraphBrowser.draw(self)
        
        # pdb.set_trace()
        
        s = self.graph.styles.default
        _ctx.reset()
        _ctx.nostroke()
        _ctx.fontsize(s.fontsize)
        
        w = s.fontsize * 2
        x = s.fontsize
        y = _ctx.HEIGHT - w - s.fontsize
        
        try:
            colors.noshadow()
        except:
            pass

        for i in range(self.sense_count):
            
            # A clicked button (i.e. the current sense)
            # has the same color as the root node.
            if i == self.sense:
                clr = self.graph.styles.root.text
            else:
                clr = s.fill
            _ctx.fill(clr)
            
            p = _ctx.rect(x, y, w, w)
            _ctx.fill(s.text)
            _ctx.align(CENTER)
            _ctx.text(str(i+1), x-w*0.5, y+s.fontsize+w*0.25, width=w*2)
            x += w * 1.1
            
            # The mouse is pressed on a button.
            if (    mousedown
                and self.graph.dragged == None
                and p.contains(MOUSEX, MOUSEY)):
                self.sense_mousedown = i
            
            # The mouse is no longer pressed on a button.    
            if (    not mousedown
                and self.sense_mousedown == i ):
                self.sense_mousedown = None
                # The mouse is released (clicked) on a button.
                if p.contains(MOUSEX, MOUSEY):
                    self.sense = i
                    self._reload(self.graph.root.id)
        
######################################################################################################

size(500, 500)
speed(30)

def setup():
    
    global wnb
    #q = str(choice(en.wordnet.all_nouns())).replace("(n.)","")
    q = "light" # colors blanket green sea work apple baby phenomenon
    wnb = WordNetBrowser()
    wnb.view(q)
 
def draw():
    
    global wnb
    wnb.draw()


