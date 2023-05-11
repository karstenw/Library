<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20230506100641.2" a="E"><vh>library</vh>
<v t="karstenw.20230506100718.1"><vh>newHeadline</vh></v>
</v>
<v t="karstenw.20230506100705.1" a="E"><vh>examples</vh>
<v t="karstenw.20230506100722.1"><vh>@clean 1_browse_wordnet.py</vh>
<v t="karstenw.20230506100740.1"><vh>Declarations</vh></v>
<v t="karstenw.20230506100740.2"><vh>class WordNetBrowser</vh>
<v t="karstenw.20230506100740.3"><vh>__init__</vh></v>
<v t="karstenw.20230506100740.4"><vh>has_node</vh></v>
<v t="karstenw.20230506100740.5"><vh>get_direct_links</vh></v>
<v t="karstenw.20230506100740.6"><vh>get_links</vh></v>
<v t="karstenw.20230506100740.7"><vh>get_branch_details</vh></v>
<v t="karstenw.20230506100740.8"><vh>_reload</vh></v>
<v t="karstenw.20230506100740.9"><vh>draw</vh></v>
</v>
<v t="karstenw.20230506100740.10"><vh>setup</vh></v>
<v t="karstenw.20230506100740.11"><vh>draw</vh></v>
</v>
<v t="karstenw.20230506100835.1" a="E"><vh>@clean 2_contextual_links.py</vh>
<v t="karstenw.20230506100912.1"><vh>Declarations</vh></v>
<v t="karstenw.20230506102028.1"><vh>loadtext</vh></v>
<v t="karstenw.20230506100912.2" a="E"><vh>class ContextualLinkBrowser</vh>
<v t="karstenw.20230506100912.3"><vh>__init__</vh></v>
<v t="karstenw.20230506100912.4"><vh>generate_filters</vh></v>
<v t="karstenw.20230506100912.5"><vh>_strip_tokens</vh></v>
<v t="karstenw.20230506100912.6"><vh>_lazy_singularize</vh></v>
<v t="karstenw.20230506100912.7"><vh>_parse_nouns</vh></v>
<v t="karstenw.20230506100912.8"><vh>has_node</vh></v>
<v t="karstenw.20230506100912.9"><vh>get_direct_links</vh></v>
<v t="karstenw.20230506100912.10"><vh>get_links</vh></v>
<v t="karstenw.20230506100912.11"><vh>get_node_descriptions</vh></v>
<v t="karstenw.20230506100912.12"><vh>_reload</vh></v>
</v>
<v t="karstenw.20230506101011.1"><vh>newHeadline</vh></v>
<v t="karstenw.20230506100912.13"><vh>setup</vh></v>
<v t="karstenw.20230506100912.14"><vh>draw</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230506100641.2"></t>
<t tx="karstenw.20230506100705.1"></t>
<t tx="karstenw.20230506100718.1"></t>
<t tx="karstenw.20230506100722.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230506100740.1"># A graph that browses through the WordNet dictionary.

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

# pdb.set_trace()

allnouns = list(wordnet.NOUNS())


</t>
<t tx="karstenw.20230506100740.10">def setup():
    
    global wnb
    #q = str(choice(en.wordnet.all_nouns())).replace("(n.)","")
    q = "light" # colors blanket green sea work apple baby phenomenon
    wnb = WordNetBrowser()
    wnb.view(q)
 
</t>
<t tx="karstenw.20230506100740.11">def draw():
    
    global wnb
    wnb.draw()


</t>
<t tx="karstenw.20230506100740.2">class WordNetBrowser(graphbrowser.GraphBrowser):
    
    """ Browse WordNet in a graph.
    
    WordNet provides extensive information on lexical relationships,
    and coupled to the gloss of each word displayed as a marquee popup 
    you get tons of factual and historical data as well.
    
    Getting data from WordNet is pretty straightforward
    but a lot of the code here is complicated to make
    the parts/specific branches in the graph clickable.
    
    """
    
    @others
######################################################################################################

size(500, 500)
speed(30)

</t>
<t tx="karstenw.20230506100740.3">def __init__(self):
    
    # Keep the word sense as a state parameter.
    graphbrowser.GraphBrowser.__init__(self)
    self.sense = 0
    self.sense_count = 0
    self.sense_mousedown = None

</t>
<t tx="karstenw.20230506100740.4">def has_node(self, node_id):

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


</t>
<t tx="karstenw.20230506100740.5">def get_direct_links(self, node_id, top=6):
    
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
            if (    len(sense) &gt; i 
                and sense[i] != node_id 
                and sense[i] not in children ):
                children.append(sense[i])
                
    children = [(5,id) for id in children]
    return children[:top]

</t>
<t tx="karstenw.20230506100740.6">def get_links(self, node_id):
    
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
                and len(n[0]) &lt; 20:
                    branch.append( (10, n[0], [label]) )
        except: pass
        #shuffle(branch)
        children.extend(branch[:top])
        
    return children

</t>
<t tx="karstenw.20230506100740.7">def get_branch_details(self, branch):
    
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
        if n.find(root) &lt; 0:
            binding = (i+4)/4*"  "
            i += 1
        children.append( (10, n, [binding]) )
        
    return children
    
</t>
<t tx="karstenw.20230506100740.8">def _reload(self, node_id, previous=None):
    
    # If the previously viewed node was
    # the details of the parts/specific branch,
    # it will be named something like "specific [root]s".
    # Strip the [root] part.
    if previous != None:
        if previous.find("specific ") == 0:
            if previous.find(node_id) &gt; 0:
                previous = "specific "
            else:
                previous = self.graph.nodes[-1].id
            self.max += 10
        if previous.find(" parts") &gt; 0:
            if previous.find(node_id) &gt; 0:
                previous = "parts "
            else:
                previous = self.graph.nodes[-1].id
    
    # If a new node is loaded, reset the current sense.
    if self.graph \
    and node_id != self.graph.root.id \
    and node_id not in ["parts ", "specific "] \
    and previous not in ["parts ", "specific "]:
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

</t>
<t tx="karstenw.20230506100740.9">def draw(self):
    
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
        if mousedown \
        and self.graph.dragged == None \
        and p.contains(MOUSEX, MOUSEY):
            self.sense_mousedown = i
        
        # The mouse is no longer pressed on a button.    
        if not mousedown \
        and self.sense_mousedown == i:
            self.sense_mousedown = None
            # The mouse is released (clicked) on a button.
            if p.contains(MOUSEX, MOUSEY):
                self.sense = i
                self._reload(self.graph.root.id)
    
</t>
<t tx="karstenw.20230506100835.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230506100912.1"># A graph that connects concepts
# based on nouns in their descriptions.

import io
import os
# import en
from os.path import basename

import linguistics
import pattern
import pattern.text
import pattern.text.en

#print("\n\nen:")
#pp(dir(pattern.text.en))

en = pattern.text.en

springgraph = ximport("springgraph")
#reload(springgraph)

graphbrowser = ximport("graphbrowser")
#reload(graphbrowser)


</t>
<t tx="karstenw.20230506100912.10">def get_links(self, node_id, treshold=1.0):
    
    children = []
    
    if node_id in self.nodes:
        
        nouns = self._parse_nouns(node_id)
        for id in self.nodes:
            if id != node_id \
            and self.nodes[id] != self.nodes[node_id]:
                # Calculate the relevance of the associated node:
                # nodes that have the node_id in their description weigh heavily,
                # nodes that have one or more of the nouns related to the node_id
                # in their description count as well.
                description = self._strip_tokens(self.nodes[id])
                count = description.count(" "+node_id+" ") * 4
                bindings = []
                for n, noun in nouns:
                    if noun in description:
                        count += 0.5
                        bindings.append(noun)
                # Limit the number of bindings and the weight
                # to avoid too strongly connected networks and node "struggling".
                bindings = bindings[:10]
                count = min(count, 6.5)
                if count &gt; treshold:
                    children.append( (count, id, bindings) )

    children.sort()
    children.reverse()
    return children[:10]

</t>
<t tx="karstenw.20230506100912.11">def get_node_descriptions(self, node_id):
    
    gnd = graphbrowser.GraphBrowser.get_node_descriptions
    msg = gnd(self, node_id)
    if len(msg) == 0:
        # Try with just the last word in the node id.
        node_id = node_id.split()[-1]
        msg = gnd(self, node_id)
    if len(msg) == 0 and node_id.find("/") &gt;= 0:
        # Try if node id are two words separated by dash.
        node_id = node_id.split("/")[-1]
        msg = gnd(self, node_id)
        
    return msg
    
</t>
<t tx="karstenw.20230506100912.12">def _reload(self, node_id, previous=None):
    
    if not node_id in self.nodes:
        if node_id.find("/") &gt;= 0:
            node_id = node_id.split("/")[-1]        
        if node_id.find(" ") &gt;= 0:
            node_id = node_id.split()[-1]
    graphbrowser.GraphBrowser._reload(self, node_id, previous)            

</t>
<t tx="karstenw.20230506100912.13">def setup():
    
    global clb
    lexicons = ["data/colors/*.txt", "data/metaphors/*.txt"]
    clb = ContextualLinkBrowser(lexicons)
    print("clb:", clb)
    clb.view("love")
    clb.generate_filters()

</t>
<t tx="karstenw.20230506100912.14">def draw():
    
    global clb
    clb.draw()

</t>
<t tx="karstenw.20230506100912.2">class ContextualLinkBrowser(graphbrowser.GraphBrowser):
    
    @others
</t>
<t tx="karstenw.20230506100912.3">def __init__(self, lexicons=[]):
    
    graphbrowser.GraphBrowser.__init__(self)
    self.graph_iterations = 5000
    self.graph_distance = 2.0
            
    self.nodes = {}
    self.cache = {}
    for lexicon in lexicons:
        for f in files(lexicon):
            n = basename(f)[:-4]
            if not n in self.nodes:
                self.nodes[n] = ""
            self.nodes[n] += " " + loadtext(f)
    
    self.link_pattern = "(JJ) NN"    
    self.filters = [
        "i", "someone", "dream", "life", 
        "situation", "and/or", "her", "type", "period", 
        "the", "an", "connotation", "side", "part", "aspect",
        "symbol", "quality", "sense", "thing", "metaphor", "trait", "person"
    ]

</t>
<t tx="karstenw.20230506100912.4">def generate_filters(self):
    
    count = {}
    for id in self.nodes.keys():
        description = self._strip_tokens(self.nodes[id])
        matches = en.sentence.find(description, "NN")
        unique_nouns = []
        for noun in matches:
            noun = noun[0][0]
            #noun = self._lazy_singularize(noun)
            if not noun in unique_nouns:
                unique_nouns.append(noun)
        for noun in unique_nouns:
            if not noun in count:
                count[noun] = 1
            else:
                count[noun] += 1

    
    count = [(count[noun], noun) for noun in count.keys()]
    count.sort()
    
    #n = len(self.nodes)
    #count = [(float(count)/n, noun) in count]
    

</t>
<t tx="karstenw.20230506100912.5">def _strip_tokens(self, str):
    
    """ Cleans up a node description string for searching.
    """
    
    str = str.lower()
    str = str.replace("."," ")
    str = str.replace(","," ")
    str = str.replace("/"," ")
    str = " "+str+" "
    return str


</t>
<t tx="karstenw.20230506100912.6">def _lazy_singularize(self, s):
    
    """ Attempts to singularize the given string.
    
    Does some straightforward inflections and checks
    with the en library if the result's plural
    is the same as the given string.
    
    """ 
    
    inflections = [
        ("ves" , "f"),
        ("ies" , "y"),
        ("es"  , ""),
        ("s"   , "")
    ]
    for pl, sg in inflections:
        singular = s.strip(pl) + sg
        if s == en.noun.plural(singular):
            if en.is_noun(singular):
                return singular
    return s


</t>
<t tx="karstenw.20230506100912.7">def _parse_nouns(self, node_id):

    """ Parses nouns from the node's description.
    
    Returns a list of nouns.
    The results are cached so next time the source text
    doesn't need to be parsed again.
    
    """

    # Parse only once,
    # next time use the parsed data stored in cache.
    # Retrieved nouns are sorted based on their count,
    # and the order in which they appeared.
    # We assume nouns that occur early in the text to be
    # more relevant than nouns that occur later.    
    if not node_id in self.cache:

        # Get each chunk of words in the description that matches the pattern.
        matches = en.sentence.find(self.nodes[node_id], self.link_pattern, chunked=False)
        strings = []
        count = {}
        for s in matches:
            # We assume the last word in the pattern is the most important.
            # We assume it is a noun.
            s = s.lower().strip("\"").split()
            noun = s[-1]
            noun = noun.strip(" ()\"'").replace("'s", "")
            noun = self._lazy_singularize(noun)
            s = " ".join(s[:-1]) + " " + noun
            s = s.strip()
            # Pick up singularized, lowercase nouns and count them.
            if  s != node_id:
                if s not in strings:
                    if noun != node_id:
                        if noun not in self.filters:
                            strings.append(s)
            if not s in count:
                count[s] = 0
            count[s] += 1
            
        sorted = []
        i = len(strings)
        for s in strings:
            sorted.append ( (count[s], i, s) )
            i -= 1
        sorted.sort()
        sorted.reverse()
        sorted = [(count, noun) for count, index, noun in sorted]
        self.cache[node_id] = sorted                    

    return self.cache[node_id]

</t>
<t tx="karstenw.20230506100912.8">def has_node(self, node_id):
    
    if node_id in self.nodes:
        return True
    return False

</t>
<t tx="karstenw.20230506100912.9">def get_direct_links(self, node_id, top=6):
 
    if node_id in self.nodes:
    
        nouns = self._parse_nouns(node_id)
        children = [(5, noun) for count, noun in nouns]
        return children[:top]
    
    else:
        
        children = []
        for id in self.nodes:
            # Any node whose description has one or several occurences
            # of the given node id is a relation to that node.
            description = self._strip_tokens(self.nodes[id])
            count = description.count(" "+node_id+" ")
            if count &gt; 0:
                children.append( (count, id) )
        children.sort()
        children.reverse()
        children = [(5, id) for count, id in children]
        return children[:int(top*1.5)]
        
</t>
<t tx="karstenw.20230506101011.1">######################################################################################################

size(500, 500)
speed(30)
clb = None

</t>
<t tx="karstenw.20230506102028.1">def loadtext( filepath ):
    result = ""
    path = os.path.abspath( filepath )
    print(filepath)
    f = io.open(path, 'r', encoding="utf-8")
    s = f.read()
    f.close()
    return s

</t>
</tnodes>
</leo_file>
