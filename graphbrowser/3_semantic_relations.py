# A graph that browses semantic relations like
# fish IsA animal
# tarbot IsExampleOf fish
# fin isPartOf fish

springgraph = ximport("springgraph")
# reload(springgraph)

graphbrowser = ximport("graphbrowser")
# reload(graphbrowser)

# import pattern.en

import os
import io
import pprint
pp=pprint.pprint

import pdb

# from os.path import basename



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
    
    def __init__(self, lexica=[]):
        
        graphbrowser.GraphBrowser.__init__(self)
        self.nodes = {}
        
        for lexicon in lexica:
            
            directory = os.path.abspath( lexicon )
            # print("path:", path)
            
            paths = files( directory + "/*.txt" )
            for path in paths:
                folder, filename = os.path.split( path )
                basename, ext = os.path.splitext( filename )

                # The file name is used as a category.
                category = basename #(f)[-4]
            
                f = io.open( path, 'r', encoding="utf-8" )
                lines = f.readlines()
                f.close()
                # rules = open(f).readlines()
                # for rule in rules:
                for line in lines:
                    
                    # A rule in the file has the following format:
                    # rulecode, concept1, concept2
                    items = line.split(",")
                    rulecode = int(items[0].strip())
                    id1 = items[1].strip()
                    id2 = items[2].strip()
                    
                    # Add new concept nodes.
                    
                    if not id1 in self.nodes:
                        self.nodes[id1] = SemanticRelationNode(id1, category)
                    if not id2 in self.nodes:
                        self.nodes[id2] = SemanticRelationNode(id2, category)
                    
                    # Build explicit relations.
                    i = int(items[0].strip())
                    self.nodes[id1].links.append( (rulecode, id2) )
                
                    # Build implicit relations.
                    if rulecode in (6, 8):
                        self.nodes[id2].links.append( (rulecode, id1) )
                    if (rulecode +80) in semantic_relations_implicit:
                        self.nodes[id2].links.append( (rulecode+80, id1) )
        # pp( self.nodes )

    def has_node(self, node_id):
    
        if node_id in self.nodes:
            return True
        else:
            return False
            
    def get_links(self, node_id):
        
        children = []
        n = self.nodes[node_id]
        for type, id in n.links:
            if type in semantic_relations_explicit:
                relation = semantic_relations_explicit[type]
            if type in semantic_relations_implicit:
                relation = semantic_relations_implicit[type]
            relation = relation.replace("_", " ")
            relation = relation.replace("is", " ").strip()
            children.append( (10, id, [relation]) )
            
        return children
        
################################################################################

size(500, 500)
speed(30)

def setup():
    
    global srb 
    lexica = [ "data/graphics", ]
    # stoopid data contents
    # lexica = [ "data/graphics", "data/colors", "data/metaphors" ]
    srb = SemanticRelationBrowser(lexica)
    names = [x for x in srb.nodes]
    # print( names )
    name = choice(names)
    # srb.view("aesthetics")
    srb.view( name )
    print(name)

def draw():
    
    global srb
    srb.draw()
