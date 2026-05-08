# A graph that connects concepts
# based on nouns in their descriptions.

import os
import io
import pprint
pp=pprint.pprint
import pdb

springgraph = ximport("springgraph")
graphbrowser = ximport("graphbrowser")

import linguistics
import pattern
from pattern.search import search
from pattern.en import parsetree, pluralize, singularize

from data import data



class ContextualLinkBrowser(graphbrowser.GraphBrowser):
    
    def __init__(self, lexicons=[]):
        
        graphbrowser.GraphBrowser.__init__(self)
        self.graph_iterations = 5000
        self.graph_distance = 2.0
                
        self.nodes = {}
        self.cache = {}
        
        for lexicon in lexicons:
            for name in lexicon:
                desc = lexicon[name]
                self.nodes[name] = " " + desc
        
        self.link_pattern = "(JJ) NN"    
        self.filters = set([
            "i", "someone", "dream", "life", 
            "situation", "and/or", "her", "type", "period", 
            "the", "an", "connotation", "side", "part", "aspect",
            "symbol", "quality", "sense", "thing", "metaphor", "trait", "person"
        ])
    
    def generate_filters(self):
        
        count = {}
        # pdb.set_trace()
        for id in self.nodes.keys():
            # print(id)
            description = self._strip_tokens(self.nodes[id])
            # matches = en.sentence.find(description, "NN")
            s = parsetree(description)
            # print('s=parsetree("%s")' % (description,) )
            matches = search("NN", s)   # all nouns
            
            # unique_nouns = []
            unique_nouns = set()
            for noun in matches:
                # noun = noun[0][0]
                noun = noun.string
                noun = self._lazy_singularize(noun)
                if not noun in unique_nouns:
                    unique_nouns.add( noun )
            for noun in unique_nouns:
                if not noun in count:
                    count[noun] = 1
                else:
                    count[noun] += 1

        
        count = [(count[noun], noun) for noun in count.keys()]
        count.sort()
        
        #n = len(self.nodes)
        #count = [(float(count)/n, noun) in count]
        
    
    def _strip_tokens(self, s):
        
        """ Cleans up a node description string for searching.
        """
        
        s = s.lower()
        s = s.replace("."," ")
        s = s.replace(","," ")
        s = s.replace("/"," ")
        s = " " + s + " "
        return s
    
    def _lazy_singularize(self, s):
        
        """ Attempts to singularize the given string.
        
        Does some straightforward inflections and checks
        with the en library if the result's plural
        is the same as the given string.
        
        """ 
        if 0:
            inflections = [
                ("ves" , "f"),
                ("ies" , "y"),
                ("es"  , ""),
                ("s"   , "")
            ]
            for pl, sg in inflections:
                singular = s.strip(pl) + sg
                if (    s == en.noun.plural(singular)
                    and en.is_noun(singular)):
                    return singular
        if 1:
            #pl = pluralize( s )
            return singularize( s )
        return s
    
    def _parse_nouns(self, node_id):

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
            
            # pdb.set_trace()
            # Get each chunk of words in the description that matches the pattern.
            #matches = en.sentence.find(self.nodes[node_id],
            #                           self.link_pattern,
            #                           chunked=False)
            s = parsetree( self.nodes[node_id] )
            print(node_id)
            print( self.nodes[node_id] )
            print()
            matches = search( self.link_pattern, s)

            strings = []
            count = {}
            for s in matches:
                # We assume the last word in the pattern is the most important.
                # We assume it is a noun.
                s = s.string
                s = s.lower().strip("\"").split()
                noun = s[-1]
                noun = noun.strip(" ()\"'").replace("'s", "")
                
                # pdb.set_trace()
                
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
    
    def has_node(self, node_id):
        
        if node_id in self.nodes:
            return True
        return False

    def get_direct_links(self, node_id, top=6):
     
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
                if count > 0:
                    children.append( (count, id) )
            children.sort()
            children.reverse()
            children = [(5, id) for count, id in children]
            return children[:int(top*1.5)]
            
    def get_links(self, node_id, treshold=1.0):
        
        children = []

        if node_id in self.nodes:

            nouns = self._parse_nouns(node_id)
            for id in self.nodes:
                if (    id != node_id
                    and self.nodes[id] != self.nodes[node_id]):
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
                    if count > treshold:
                        children.append( (count, id, bindings) )

        children.sort()
        children.reverse()
        return children[:10]

    def get_node_descriptions(self, node_id):
        
        gnd = graphbrowser.GraphBrowser.get_node_descriptions
        msg = gnd(self, node_id)
        if len(msg) == 0:
            # Try with just the last word in the node id.
            node_id = node_id.split()[-1]
            msg = gnd(self, node_id)
        if len(msg) == 0 and node_id.find("/") >= 0:
            # Try if node id are two words separated by dash.
            node_id = node_id.split("/")[-1]
            msg = gnd(self, node_id)
            
        return msg
        
    def _reload(self, node_id, previous=None):
        
        if not node_id in self.nodes:
            if node_id.find("/") >= 0:
                node_id = node_id.split("/")[-1]
            if node_id.find(" ") >= 0:
                node_id = node_id.split()[-1]
        graphbrowser.GraphBrowser._reload(self, node_id, previous)

########################################################################################

size(800, 800)
speed(30)
clb = None

def setup():
    
    global clb
    
    lexicons = [ data['colors'], data['metaphors'] ]
    clb = ContextualLinkBrowser( lexicons )
    if 0:
        query = choice( list(clb.nodes.keys()) )
        clb.view( query )
    else:
        clb.view( "love" )
    clb.generate_filters()

def draw():
    
    global clb
    clb.draw()

