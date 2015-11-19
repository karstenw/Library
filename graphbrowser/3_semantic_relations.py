# A graph that browses semantic relations like
# fish IsA animal
# tarbot IsExampleOf fish
# fin isPartOf fish

springgraph = ximport("springgraph")
reload(springgraph)

graphbrowser = ximport("graphbrowser")
reload(graphbrowser)

import en
from os.path import basename

semantic_relations_explicit = {
    1   : "is_property_of",
    2   : "is_part_of",
    3   : "is_a",
    4   : "is_used_for",
    5   : "is_made_of",
    6   : "is_related_to",
    7   : "is_example_of",
    8   : "is_opposed_to",
    9   : "is_capable_of",
    10  : "is_desired_effect_of"
}

# Don't use these ones in rule files,
# they're derived automatically.
semantic_relations_implicit = {
    81  : "has_property",
    82  : "has_part",
    83  : "concrete_form",
    84  : "desired_result_of",
    87  : "has_example",
    89  : "implemented_by",
    90  : "has_possible_cause",                            
}

class SemanticRelationNode:
    
    def __init__(self, id, category=""):
        
        self.id = id
        self.category = category
        self.links = []

class SemanticRelationBrowser(graphbrowser.GraphBrowser):
    
    def __init__(self, lexicon=[]):
        
        graphbrowser.GraphBrowser.__init__(self)
        self.nodes = {}
        
        for f in files(lexicon):
            
            # The file name is used as a category.
            category = basename(f)[-4]
            
            rules = open(f).readlines()
            for rule in rules:
                
                # A rule in the file has the following format:
                # rulecode, concept1, concept2
                rule = rule.split(",")
                id1 = rule[1].strip()
                id2 = rule[2].strip()
                
                # Add new concept nodes.
                if not self.nodes.has_key(id1): 
                    self.nodes[id1] = SemanticRelationNode(id1, category)
                if not self.nodes.has_key(id2): 
                    self.nodes[id2] = SemanticRelationNode(id2, category)
            
                # Build explicit relations.
                i = int(rule[0].strip())
                self.nodes[id1].links.append( (i, id2) )
                
                # Build implicit relations.
                if i == 6 or i == 8:
                    self.nodes[id2].links.append( (i, id1) )
                if semantic_relations_implicit.has_key(i+80):
                    self.nodes[id2].links.append( (i+80, id1) )
                 
    def has_node(self, node_id):
    
        if self.nodes.has_key(node_id):
            return True
        else:
            return False
            
    def get_links(self, node_id):
        
        children = []
        n = self.nodes[node_id]
        for type, id in n.links:
            if semantic_relations_explicit.has_key(type):
                relation = semantic_relations_explicit[type]
            if semantic_relations_implicit.has_key(type):
                relation = semantic_relations_implicit[type]
            relation = relation.replace("_", " ")
            relation = relation.replace("is", " ").strip()
            children.append( (10, id, [relation]) )
            
        return children
        
######################################################################################################

size(500, 500)
speed(30)

def setup():
    
    global srb 
    lexicon = "data/graphics/*.txt"
    srb = SemanticRelationBrowser(lexicon)
    srb.view("aesthetics")
 
def draw():
    
    global srb
    srb.draw()