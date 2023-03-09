# A graph that connects concepts
# based on nouns in their descriptions.

import os
import io
import pprint
pp=pprint.pprint

springgraph = ximport("springgraph")
#reload(springgraph)

graphbrowser = ximport("graphbrowser")
#reload(graphbrowser)


import pattern
import pattern.text
import pattern.text.en

#print("\n\nen:")
#pp(dir(pattern.text.en))

en = pattern.text.en

# import en
from os.path import basename

class ContextualLinkBrowser(graphbrowser.GraphBrowser):
    
    def __init__(self, lexicons=[]):
        
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
                path = os.path.abspath( f )
                # print("path:", path)
                fob = io.open( path, "r", encoding="utf-8" )
                s = fob.read()
                fob.close()
                self.nodes[n] += " " + s
        
        self.link_pattern = "(JJ) NN"    
        self.filters = [
            "i", "someone", "dream", "life", 
            "situation", "and/or", "her", "type", "period", 
            "the", "an", "connotation", "side", "part", "aspect",
            "symbol", "quality", "sense", "thing", "metaphor", "trait", "person"
        ]
    
    def generate_filters(self):
        
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

            # Get each chunk of words in the description that matches the pattern.
            matches = en.sentence.find(self.nodes[node_id],
                                       self.link_pattern,
                                       chunked=False)
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
                if  s != node_id \
                and s not in strings \
                and noun != node_id \
                and noun not in self.filters:
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
        
        #if node_id in self.nodes:
        return True
    
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
                if count > 0: children.append( (count, id) )
            children.sort()
            children.reverse()
            children = [(5, id) for count, id in children]
            return children[:int(top*1.5)]
            
    def get_links(self, node_id, treshold=1.0):
        
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

######################################################################################################

size(500, 500)
lexicons = ["data/colors/*.txt", "data/metaphors/*.txt"]
clb = ContextualLinkBrowser(lexicons)
print("clb:", clb)
clb.view("love")
clb.generate_filters()

