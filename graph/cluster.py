# Copyright (c) 2007 Tom De Smedt.
# See LICENSE.txt for details.

from types import FunctionType, LambdaType

# py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def sortlist(thelist, thecompare):
    if py3:
        sortkeyfunction = cmp_to_key( thecompare )
        thelist.sort( key=sortkeyfunction )
    else:
        thelist.sort( thecompare )


class FlowerWord:
    def __init__(self, word):
        # pdb.set_trace()
        self.word = word
        self.synsets = wordnet.synsets( word )
        self.idx = 0
        self.antonym = ""
        self.gloss = ""
        self.synset = None
        self.synonyms = []
        self.antonym = ""
        self.gloss = ""
        self.lexname = ""

        if len(self.synsets) > 0:
            synonyms = self.synsets[0].synonyms
            try:
                self.idx = synonyms.index(word)
                w = self.synset = self.synsets[self.idx]
                #print("Found synset:", w)
            except:
                w = self.synsets[0]
                #print("Use synset:", w)

            self.antonym = w.antonym
            self.gloss = w.gloss
            self.lexname = w.lexname

    def hyponyms(self):
        result = []
        for synset in self.synsets:
            hyponyms = synset.hyponyms()
            for hyponym in hyponyms:
                synonyms = hyponym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result

    def hypernyms(self):
        result = []
        for synset in self.synsets:
            hypernyms = synset.hypernyms()
            for hypernym in hypernyms:
                synonyms = hypernym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result


    def senses(self):
        result = []
        for synset in self.synsets:
            senses = synset.senses
            result.append( senses )
        return result


    def holonyms(self):
        result = []
        for synset in self.synsets:
            holonyms = synset.holonyms()
            for holonym in holonyms:
                synonyms = hyponym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result

    def meronyms(self):
        result = []
        for synset in self.synsets:
            meronyms = synset.meronyms()
            for meronym in meronyms:
                synonyms = hyponym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result



def sortnodes_zero( a, b ):
    if a[0] > b[0]:
        return 1
    elif a[0] < b[0]:
        return -1
    return 0

#--- LIST OPERATIONS ---------------------------------------------------------------------------------

def sorted(thelist, cmp=None, reversed=False):
    """ Returns a sorted copy of the list.
    """
    thelist = [x for x in thelist]
    # thelist.sort(cmp)
    sortlist(thelist, cmp)
    if reversed:
        thelist.reverse()
    return thelist


def unique( thelist ):
    """ Returns a copy of the list without duplicates.
    """
    unique = []
    [unique.append(x) for x in thelist if x not in unique]
    return unique


#--- SET THEORY --------------------------------------------------------------------------------------

def flatten(node, distance=1):
    
    """ Recursively lists the node and its links.
    
    Distance of 0 will return the given [node].
    Distance of 1 will return a list of the node and all its links.
    Distance of 2 will also include the linked nodes' links, etc.
    
    """
    
    # When you pass a graph it returns all the node id's in it.
    if hasattr(node, "nodes") and hasattr(node, "edges"):
        return [n.id for n in node.nodes]
    
    all = [node]
    if distance >= 1:
        for n in node.links: 
            all += n.flatten(distance-1)
    
    return unique(all)
    
def intersection(a, b):
    """ Returns the intersection of lists.
    a & b -> elements that appear in a as well as in b.
    """
    return filter(lambda x: x in a, b)
    
    
def union(a, b):
    """ Returns the union of lists.
    a | b -> all elements from a and all the elements from b.
    """     
    return a + filter(lambda x: x not in a, b)

def difference(a, b):
    """ Returns the difference of lists.
    a - b -> elements that appear in a but not in b.
    """
    return filter(lambda x: x not in b, a)
    
#--- SUBGRAPH ----------------------------------------------------------------------------------------

def subgraph(graph, id, distance=1):
    
    """ Creates the subgraph of the flattened node with given id (or list of id's).
    Finds all the edges between the nodes that make up the subgraph.
    """
    
    g = graph.copy(empty=True)
    
    if isinstance(id, (FunctionType, LambdaType)):
        # id can also be a lambda or function that returns True or False
        # for each node in the graph. We take the id's of nodes that pass.
        id = [node.id for node in filter(id, graph.nodes)]
    if not isinstance(id, (list, tuple)):
        id = [id]
    for id in id:
        for n in flatten(graph[id], distance):
            g.add_node(n.id, n.r, n.style, n.category, n.label, (n==graph.root), n.__dict__)
        
    for e in graph.edges:
        if (    e.node1.id in g
            and e.node2.id in g ):
            g.add_edge(e.node1.id, e.node2.id, e.weight,
                       e.length, e.label, e.__dict__)
    
    # Should we look for shortest paths between nodes here?
    
    return g
 
#--- CLIQUE ----------------------------------------------------------------------------------------
 
def is_clique(graph):
    
    """ A clique is a set of nodes in which each node is connected to all other nodes.
    """
    
    #for n1 in graph.nodes:
    #    for n2 in graph.nodes:
    #        if n1 != n2 and graph.edge(n1.id, n2.id) == None:
    #            return False

    if graph.density < 1.0: 
        return False
    
    return True
    
def clique(graph, id):
    
    """ Returns the largest possible clique for the node with given id.
    """
    
    clique = [id]
    for n in graph.nodes:
        friend = True
        for id in clique:
            if n.id == id or graph.edge(n.id, id) == None:
                friend = False
                break
        if friend:
            clique.append(n.id)
    
    return clique
    
def cliques(graph, threshold=3):
    
    """ Returns all the cliques in the graph of at least the given size.
    """
    
    cliques = []
    for n in graph.nodes:
        c = clique(graph, n.id)
        if len(c) >= threshold: 
            c.sort()
            if c not in cliques:
                cliques.append(c)
    
    return cliques

#--- UNCONNECTED SUBGRAPHS -------------------------------------------------------------------------

def partition(graph):
    
    """ Splits unconnected subgraphs.
    
    For each node in the graph, make a list of its id and all directly connected id's.
    If one of the nodes in this list intersects with a subgraph,
    they are all part of that subgraph.
    Otherwise, this list is part of a new subgraph.
    Return a list of subgraphs sorted by size (biggest-first).
    
    """
    
    g = []
    for n in graph.nodes:
        c = [n.id for n in flatten(n)]
        f = False
        for i in range(len(g)):
            if len(intersection(g[i], c)) > 0:
                g[i] = union(g[i], c)
                f = True
                break
        if not f:
            g.append(c)
    
    # If 1 is directly connected to 2 and 3,
    # and 4 is directly connected to 5 and 6, these are separate subgraphs.
    # If we later find that 7 is directly connected to 3 and 6,
    # it will be attached to [1, 2, 3] yielding
    # [1, 2, 3, 6, 7] and [4, 5, 6].
    # These two subgraphs are connected and need to be merged.
    merged = []
    for i in range(len(g)):
        merged.append(g[i])
        for j in range(i+1, len(g)):
            if len(intersection(g[i], g[j])) > 0:
                merged[-1].extend(g[j])
                g[j] = []
    
    g = merged
    g = [graph.sub(g, distance=0) for g in g]
    g.sort(lambda a, b: len(b) - len(a))
    
    return g

