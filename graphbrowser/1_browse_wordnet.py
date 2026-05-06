# A graph that browses through the WordNet dictionary.

import os
import pdb
kwdbg = True
kwlog = True


springgraph = ximport("springgraph")
#reload(springgraph)

graphbrowser = ximport("graphbrowser")
#reload(graphbrowser)

import linguistics
FlowerWord = linguistics.FlowerWord.FlowerWord

import pattern
import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = pattern.text.en.wordnet

from pattern.en import pluralize

from random import shuffle

import pdb
import pprint
pp=pprint.pprint

allnouns = list(wordnet.NOUNS())


gSenses = dict()
gRootword = ""
gSenseindex = 0


#### REPLACEMENTS ##############################################################
# 
# these should move two levels up into linguistics


def holonym( word, sense="", all=False ):
    fw = FlowerWord( word )
    hn = fw.holonyms()
    if all:
        return hn
    if len(hn) > 0:
        return hn[0]
    return ""

def meronym( word, sense="", all=False ):
    fw = FlowerWord( word )
    mn = fw.meronyms()
    if all:
        return mn
    if len(mn) > 0:
        return mn[0]
    return ""

def antonym( word, sense="", all=False ):
    fw = FlowerWord( word )
    an = fw.antonym
    if 0: #len(an) > 0:
        print("antonym(%s): %s" % (word, str(an)))
    if all:
        return an
    if len(an) > 0:
        return an[0].antonym
    return ""

def hypernym( word, sense="", all=False ):
    fw = FlowerWord( word )
    hn = fw.hypernyms()
    if all:
        return hn
    if len(hn) > 0:
        return hn[0]
    return ""

def fsenses( word, sense="", all=False ):
    fw = FlowerWord( word )
    sn = fw.senses()
    print("senses(%s): %s" % (word, str(sn)))
    if all:
        return sn
    if len(sn) > 0:
        return sn[0]
    return ""

def hyponym( word, sense="", all=False ):
    fw = FlowerWord( word )
    hn = fw.hyponyms()
    if all:
        return hn
    if len(hn) > 0:
        return hn[0]
    return ""


class WordNetBrowser(graphbrowser.GraphBrowser):
    
    """ Browse WordNet in a graph.
    
    WordNet provides extensive information on lexical relationships, and coupled
    to the gloss of each word displayed as a marquee popup you get tons of
    factual and historical data as well.
    
    Getting data from WordNet is pretty straightforward but a lot of the code
    here is complicated to make the parts/specific branches in the graph clickable.
    
    """
    
    def __init__(self):
        
        # Keep the word sense as a state parameter.
        # pdb.set_trace()
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
        # senses = wordnet.synsets( node_id ).senses
        senses = FlowerWord( node_id ).senses()
        
        if 0:
            for i in range( 2 ):
                for sense in senses:
                    if (    len(senses) > i 
                        and sense[i] != node_id 
                        and sense[i] not in children ):
                        children.append(sense[i])
                    
        # children = [(5,id) for id in children]
        children = [(5,id) for id in senses]
        return children[:top]


    def get_links(self, node_id):
        
        print("get_links:", node_id)
        
        # pdb.set_trace()
        
        if node_id == "specific ":
            return self.get_branch_details("hyponym")
        if node_id == "parts ":
            return self.get_branch_details("holonym")
        
        children = []
        # lexname = en.noun.lexname(node_id)
        lexname = FlowerWord(node_id).lexname
        if lexname != "":
            children.append( (1, lexname, ["category "]) )
        
        branches = [
            # TODO: kill these function pointers
            (6, holonym  , "parts "),
            (2, meronym  , "part of "),
            (2, antonym  , "opposite "),
            (3, hypernym , "generic "),
            (2, fsenses   , "action "),
            (6, hyponym  , "specific "),
        ]
        # For each of the branches, get all the words from WordNet.
        # Exclude long words.
        # Shuffle the list and then take the top.
        for top, f, label in branches:
            branch = set()
            # The lookup for verb senses might not work with a noun,
            # then we get idiotic error stuff like:
            # KeyError: "'florenz ziegfeld' is not in the 'verb' database"
            try:
                if 0:
                    for name in f(node_id): #, sense=self.sense):
                        if (    name[0] != node_id
                            and name[0] not in branch
                            and len(name[0]) < 20 ):
                            branch.append( (10, name[0], [label]) )
                if 1:
                    for name in f(node_id, all=True): #, sense=self.sense):
                        if (    name != node_id
                            and len(name) < 20 ):
                            record = (10, name, (label,) )
                            branch.add( record )
            except:
                pass
            branch = list( branch )
            shuffle(branch)
            children.extend(branch[:top])
            
        return children

    def get_branch_details(self, branch):
        
        """ Fetches data when clicked on the parts/specific branches.
        """
        
        root = self.graph.nodes[0].id.lower()
        # f = getattr(en.noun, branch)
        
        # This is more readable:
        if branch == "hyponym": f = hyponym
        if branch == "holonym": f = holonym
        
        unique = set()
        for name in f(root, all=True): #, sense=self.sense):
            # if name[0] not in unique:
            # unique.add(name[0])
            unique.add( name )
        unique = list( unique )
        shuffle(unique)
        
        children = []
        i = 0
        for name in unique:
            # Organise connected nodes in branches,
            # each branch carries 4 nodes.
            # Nodes that have the root id in their own id,
            # form a branch on their own.
            binding = " "
            if name.find(root) < 0:
                binding = (i+4) / 4 * "  "
                i += 1
            children.append( (10, name, [binding]) )
            
        return children



    def _reload(self, node_id, previous=None):
        global gSenses, gRootword, gSenseindex
        
        if 1:
            print("node_id:", node_id)
            print("gRootword:", gRootword)
            print("gSenseindex:", gSenseindex)
        #if node_id in ("visible_radiation", ):
        #    pdb.set_trace()
        
        # If the previously viewed node was
        # the details of the parts/specific branch,
        # it will be named something like "specific [root]s".
        # Strip the [root] part.
        if previous != None:
            
            # pdb.set_trace()
            
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
        
        # pdb.set_trace()
        
        # self.sense > 0 if tab clicked
        # self.sense == 0 if node clicked
        
        if node_id in gSenses:
            senses = gSenses[node_id]
        else:
            senses = FlowerWord( node_id ).senses()
        
        self.sense_count = len( senses )
        
        if self.sense > 0:
            if self.sense < len( senses ):
                node_id = senses[self.sense]
            else:
                pass
        
        graphbrowser.GraphBrowser._reload(self, node_id, previous)
        
        
        try:
            self.sense = senses.index( node_id )
            
        except:
            self.sense = 0
            
        # Get the number of senses of this node.
        # Find the node in the graph matching that sense.
        # It's one of the nodes directly connected to the root.
        # Mark it with an appropriate style.
        
        """
        try:
            senses = FlowerWord( node_id ).senses() #en.noun.senses(node_id)
            self.sense_count = len( senses )
            for word in senses: #[self.sense]:
                if word != self.graph.root.id:
                    node = self.graph.node(word)
                    if node:
                        node.style = springgraph.STYLE_MARKED
        except Exception as err:
            print("SILENT ERROR:", err)
            self.sense_count = 0
        """
        
        # If the current viewed node is
        # the details of the parts/specific branch,
        # format the root name like "specific [root]s"
        # instead of just "specific".
        root = self.graph.root
        if root.id == "specific ": 
            root.id += pluralize( previous ) #en.noun.plural(previous)
            self.max -= 10
        if root.id == "parts ": 
            root.id = previous+" parts"


    def draw(self):
        """ Additional drawing and events for sense selection buttons.
        """
        global gSenses, gRootword, gSenseindex
        
        graphbrowser.GraphBrowser.draw(self)
        
        # pdb.set_trace()
        
        try:
            s = self.graph.styles.default
        except Exception as err:
            # pdb.set_trace()
            print("draw().style ERR:", err)
            print(dir(self.graph))
        _ctx.reset()
        _ctx.nostroke()
        try:
            _ctx.fontsize(s.fontsize)
        except Exception:
            _ctx.fontsize( 9 )
        
        w = s.fontsize * 2
        x = s.fontsize
        y = _ctx.HEIGHT - w - s.fontsize
        
        try:
            colors.noshadow()
        except:
            pass
        
        # draw the tabs
        for i in range(self.sense_count):
            
            # A clicked button (i.e. the current sense)
            # has the same color as the root node.
            if i == self.sense:
                clr = self.graph.styles.root.text
            else:
                clr = s.fill
            _ctx.fill(clr)
            
            rectpath = _ctx.rect(x, y, w, w)
            _ctx.fill(s.text)
            _ctx.align(CENTER)
            _ctx.text(str(i+1), x-w*0.5, y+s.fontsize+w*0.25, width=w*2)
            x += w * 1.1
            
            # The mouse is pressed on a button.
            if (    mousedown
                and self.graph.dragged == None
                and rectpath.contains(MOUSEX, MOUSEY)):
                self.sense_mousedown = i
            
            # The mouse is no longer pressed on a button.    
            if (    not mousedown
                and self.sense_mousedown == i ):
                self.sense_mousedown = None
                # The mouse is released (clicked) on a button.
                if rectpath.contains(MOUSEX, MOUSEY):
                    self.sense = gSenseindex = i
                    gRootword = self.graph.root.id
                    self._reload(self.graph.root.id)


####################################################################################

size( 650, 650 )
speed(30)

def setup():
    
    global wnb, gSenses, gRootword, gSenseindex
    
    # lets have at least 2 senses
    # gSenses = []
    count = 0
    q = "light"
    senses = fsenses( q, all=True )
    gSenses[q] = senses
    gRootword = q
    while False:
        q = str( choice( allnouns)).replace("(n.)","" )
        print("TRY q:", q )
        senses = fsenses( q )
        if len( senses ) > 1:
            gSenses[q] = senses
            gRootword = q
            gSenseindex = 0
            break
    
    # q = "light" # colors blanket green sea work apple baby phenomenon
    wnb = WordNetBrowser()
    wnb.view(q)
 
def draw():
    
    global wnb
    wnb.draw()
