# A graph that browses through the WordNet dictionary.
# You can click on nodes (including "has-parts" and "has-specific").
# You'll need the NodeBox Linguistics library installed.
# Author: Tom De Smedt.


import os
import pdb
kwdbg = False
kwlog = False

try:
    graph = ximport("graph")
except ImportError:
    graph = ximport("__init__")


from random import shuffle

import linguistics
import FlowerWord
FlowerWord = FlowerWord.FlowerWord

# from linguistics import FlowerWord

import pattern
import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = pattern.text.en.wordnet

allnouns = list( wordnet.NOUNS() )
nouns = set( allnouns )



#### REPLACEMENTS ##############################################################
# 
# these should move two levels up into linguistics


def holonym( word, sense="", all=False ):
    fw = FlowerWord( word )
    hn = fw.holonyms()
    #print("holonym(%s): %s" % (word, str(hn)))
    if all:
        return hn
    if len(hn) > 0:
        return hn[0]
    return ""

def meronym( word, sense="", all=False ):
    fw = FlowerWord( word )
    mn = fw.meronyms()
    #print("meronym(%s): %s" % (word, str(mn)))
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
        #print("antonym(%s): %s" % (word, str(an[0].antonym)))
        return an[0].antonym
    return ""

def hypernym( word, sense="", all=False ):
    fw = FlowerWord( word )
    hn = fw.hypernyms()
    #print("hypernym(%s): %s" % (word, str(hn)))
    if all:
        return hn
    if len(hn) > 0:
        return hn[0]
    return ""

def fsenses( word, sense="", all=False ):
    fw = FlowerWord( word )
    sn = fw.senses()
    if kwlog:
        print("senses(%s): %s" % (word, str(sn)))
    if all:
        return sn
    if len(sn) > 0:
        return sn[0]
    return ""

def hyponym( word, sense="", all=False ):
    fw = FlowerWord( word )
    hn = fw.hyponyms()
    #print("hyponym(%s): %s" % (word, str(hn)))
    if all:
        return hn
    if len(hn) > 0:
        return hn[0]
    return ""


#### WORDNET GRAPH #############################################################

class wordnetgraph(graph.graph):
    
    """ Browse WordNet in a graph.
    
    The wordnetgraph class is based on the standard graph class.
    I've added some functionality to fetch data from WordNet and browse
    through it.  When you click on a node, the wordnetgraph.click() method
    is fired.  This will check if the clicked node is a noun in WordNet, and
    if so, reload the graph's nodes and connections with that noun at the root.
    
    The main methods, get_senses() and get_relations(),
    are called when the graph reloads.
    They retrieve data from WordNet and format it as nodes.
    The expand() method is called when you click on "has-specific" or "has-parts".
    
    A helper class, SenseButtons, draws the interactive word sense selection buttons.
    
    """
    
    def __init__(self, iterations=2000, distance=1.3):
        
        graph.graph.__init__(self, iterations, distance)
        self.styles = graph.create().styles
        self.events.click = self.click
        self.events.popup = True
        
        # Display a maximum of 20 nodes.
        self.max = 20
        
        # A row of buttons to select the current word sense.
        self.senses = SenseButtons(self, 20, 20)

    def is_expandable(self, id):
        
        """ Some of the branches are expandable:
        if you click on has-parts or has-specific, a detailed view will load.
        """
        
        if id in ["has-parts", "has-specific"]: 
            return True
        else:
            return False

    def is_clickable(self, node):
        
        """ Every node that is a noun is clickable (except the root).
        """
        
        
        if node == self.root:
            return False

        id = node.id.lower()
        if id in nouns:
            return True
        if self.is_expandable(node.id):
            return True
        return False


    def get_senses(self, word, top=12):

        """ The graph displays the different senses of a noun,
        e.g. light -> lighter, luminosity, sparkle, ...
        """
        
        word = str(word)
        # word = word.replace( "_", " " )
        
        if self.is_expandable(word):
            return []
        
        # If there are 4 word senses and each of it a list of words,
        # take the first word from each list, then take the second etc.
        words = []
        
        fw = FlowerWord( word )
        snses = fw.senses()
        if 0:
            # i think this is for a different structure
            for i in range(2):
                for sense in snses: #en.noun.senses(word):
                    if (    len(sense) > i
                        and sense[i] != word
                        and sense[i] not in words):
                        words.append(sense[i])
                    
        #return words[:top]
        return snses[:top]
    
    
    def get_relations(self, word, previous=None):
        
        """ The graph displays semantic relations for a noun,
        e.g. light -> has-specific -> candlelight.
        """
        
        word = str(word)
        
        if self.is_expandable(word):
            print("get_relations.is_expandable:", word)
            return self.expand(word, previous)
        
        words = []
        
        fw = FlowerWord( word )
        # lexname = en.noun.lexname(word)
        lexname = fw.lexname
        if lexname != "":
            words.append( (lexname, "category ") )
        
        relations = [
            # (6, en.noun.holonym  , "has-parts"),
            (6, holonym  , "has-parts"),
            (3, meronym  , "is-part-of"),
            (2, antonym  , "is-opposite-of"),
            (4, hypernym , "is-a"),
            (3, fsenses   , "is-action"),
            (6, hyponym  , "has-specific"),
        ]
        # Get related words from WordNet.
        # Exclude long words and take the top of the list.
        
        for top, f, relation in relations:
            result = []
            try:
                wordlist = f(word, sense=self.senses.current, all=True)
            except:
                try:
                    wordlist = f(word, all=True)
                except:
                    continue
            if wordlist is None:
                wordlist = []
            # old
            if 0:
                for w in wordlist:
                    if (    w != word
                        and w not in result
                        and len(w) < 20):
                        result.append( (w, relation) )
            # rewritten
            if 1:
                for w in wordlist:
                    if w != word:
                        if w not in result:
                            if len(w) < 20:
                                result.append( (w, relation) )
            words.extend( result ) #[:top] )
        if kwdbg:
            print("get_relations(%s): %s" % (word, str(words)))
        return words

    def expand(self, relation, previous=None):
        
        """ Zoom in to the hyponym or holonym branch.
        """
        
        if relation == "has-specific" : f = hyponym # en.noun.hyponym
        if relation == "has-parts"    : f = holonym # en.noun.holonym
        
        root = str(self.root.id.lower())
        unique = []
        if previous: previous = str(previous)
        for w in f(previous, sense=self.senses.current):
            if w[0] not in unique: unique.append(w[0])
        shuffle(unique)
        
        words = []
        i = 0
        for w in unique:
            # Organise connected nodes in branches of 4 nodes each.
            # Nodes that have the root id in their own id,
            # form a branch on their own.
            label = " "
            if w.find(root) < 0:
                label = (i+4) / 4 * "  "
                i += 1
            words.append((w, label))
            
        return words

    def click(self, node):
        
        """ If the node is indeed clickable, load it.
        """
        
        if self.is_clickable(node):
            p = self.root.id
            # Use the previous back node instead of "has specific".
            if self.is_expandable(p):
                p = self.nodes[-1].id
            self.load(node.id, previous=p)


    def load(self, word, previous=None):
        
        self.clear()
        
        word = str(word)
        
        # Add the root (the clicked node) with the ROOT style.
        self.add_node(word, root=True, style="root")
        
        # Add the word senses to the root in the LIGHT style.
        senses = self.get_senses(word)
        for wrd in senses:
            self.add_node(wrd, style=self.styles.light.name)
            self.add_edge(word, wrd, 0.5)
            
            if len(self) > self.max:
                break
        
        # Add relation branches to the root in the DARK style.
        for wrd, rel in self.get_relations(word, previous):
            
            if type(rel) in (list,):
                # pdb.set_trace()
                pass
            
            if type(wrd) in (list,):
                # pdb.set_trace()
                for wrd2 in wrd:
                    self.add_edge( wrd2, rel, 1.0)
            else:
                self.add_edge( wrd, rel, 1.0)
                
            self.add_node( rel, style="dark")
            self.add_edge( word, rel)
            
            """
                self.add_node( rel, style="dark")
                self.add_edge( word, rel)
            """

            if len(self) > self.max:
                break
        
        # Provide a back link to the previous word.
        if (    previous
            and previous != self.root.id):
            n = self.add_node(previous, 10)
            if len(n.links) == 0:
                self.add_edge(word, n.id)
            n.style = "back"
        
        # Indicate the word corresponding to the current sense.
        if self.senses.count() > 0:
            #for w in en.noun.senses(word)[self.senses.current]:
            for word in gSenses: #fsenses(word, all=True)[self.senses.current]:
                
                node = self.node(word)
                if node and node != self.root: 
                    node.style = "marked"


    def draw(self, *args, **kwargs):
        
        """ Additional drawing for sense selection buttons.
        """
        
        graph.graph.draw(self, *args, **kwargs)
        self.senses.draw()

### WORD SENSE SELECTION #######################################################

class SenseButtons:
    
    """ A row of word sense selection buttons.
    """
    
    def __init__(self, graph, x, y):
        
        self.graph = graph
        self.word = ""
        self.senses = None
        self.x = x
        self.y = y
        
        self.current = 0
        self.pressed = None

    def count(self):
        
        """ The number of senses for the current word.
        The current word is synched to the graph's root node.
        """
        
        if self.word != self.graph.root.id:
            self.word = str(self.graph.root.id)
            self.current = 0
            self._count = 0
            if self.senses is None:
                self.senses = gSenses # fsenses(self.word, all=True)
            self._count = len( self.senses )
            try:
                self.current = self.senses.index( self.word )
            except:
                pass
            if 0:
                # try: self._count = len(en.noun.senses(self.word))
                try:
                    self._count = len( gSenses ) #fsenses(self.word, all=True) )
                except:
                    pass
                
        return self._count

    def draw(self):
        
        s = self.graph.styles.default
        x, y, f = self.x, self.y, s.fontsize
        
        _ctx.reset()
        _ctx.nostroke()
        _ctx.fontsize(f)
        
        for i in range(self.count()):
            
            clr = s.fill
            if i == self.current:
                clr = self.graph.styles.default.background
            _ctx.fill(clr)
            p = _ctx.rect(x, y, f*2, f*2)
            _ctx.fill(s.text)
            _ctx.align(CENTER)
            _ctx.text(str(i+1), x-f, y+f*1.5, width=f*4)
            x += f * 2.2
            
            self.log_pressed(p, i)
            self.log_clicked(p, i)

    def log_pressed(self, path, i):
        
        """ Update senses.pressed to the last button pressed.
        """
        
        if (    mousedown 
            and self.graph.events.dragged == None 
            and path.contains(MOUSEX, MOUSEY)):
            self.pressed = i

    def log_clicked(self, path, i):
        
        """ Update senses.current to the last button clicked.
        """
        
        if not mousedown and self.pressed == i:
            self.pressed = None
            if path.contains(MOUSEX, MOUSEY):
                self.current = i
                if 0:
                    self.graph.load( self.graph.root.id )
                else:
                    self.graph.load( self.senses[i] )
        
######################################################################################################

query = "house"
query = "rhetoric"
query = choice( allnouns )
goodies = ("inconvenience", "biology", "cyberpunk", "frankfurt", "computer",
           "monastery", "africa", "rhetoric")

query = choice( goodies )
# query = "biology"

g = wordnetgraph(distance=1.2)
if kwlog:
    print( "query:", query )
gSenses = fsenses( query, all=True )
g.load(query)

size(850, 750)
speed(30) 
def draw():
    g.styles.textwidth = 160
    g.draw(
        directed=True, 
        weighted=True,
        traffic=True
    )
    
