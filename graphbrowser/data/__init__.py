

# load the data folders in a faster way

import os
import io
import glob
import pprint
pp=pprint.pprint

import pdb

# pdb.set_trace()

base, _ = os.path.split( __file__ )
lexica = ("colors", "graphics", "metaphors" )

def loaddatafolders():
    for lexicon in lexica:
        directory = os.path.abspath( os.path.join( base, lexicon ))
        root, parent = os.path.split( directory )
        # print("directory:", directory)
        outpath = os.path.join( base, parent + ".tab" )
        if os.path.exists( outpath ):
            continue
        
        out = open(outpath, 'w')
        
        paths = glob.glob( directory + "/*.txt" )
        
        for path in paths:
            folder, filename = os.path.split( path )
            basename, ext = os.path.splitext( filename )
            
            # The file name is used as a category.
            category = basename
            
            f = io.open( path, 'r', encoding="utf-8" )
            lines = f.readlines()
            f.close()
            
            for line in lines:
                
                if lexicon == "graphics":
                    # A rule in the file has the following format:
                    # rulecode, concept1, concept2
                    
                    items = line.split(",")
                    
                    rulecode = items[0].strip()
                    id1 = items[1].strip()
                    id2 = items[2].strip()
                    s = "%s\t%s\t%s\t%s\n"
                    out.write( s % (category, rulecode, id1, id2))
                elif lexicon in( "colors", "metaphors"):
                    line = line.rstrip()
                    line = line.replace("<li>", "").replace("</li>", "").replace("<ol>", "").replace("</ol>", "")
                    s = "%s\t%s\n"
                    out.write( s % (basename, line) )
                else:
                    # should not happen
                    pdb.set_trace()
        out.close()


def lexicas():
    result = dict(
        colors=dict(),
        graphics=dict(),
        metaphors=dict())
    
    # pdb.set_trace()
    
    for lexicon in lexica:
        directory = os.path.abspath( os.path.join( base, lexicon ))
        root, parent = os.path.split( directory )
        # print("directory:", directory)
        inpath = os.path.join( base, parent + ".tab" )
        f = open( inpath, 'r' )
        for line in f:
            line = line.rstrip()
            category, rest = line.split('\t', 1)
            
            if lexicon == "graphics":
                if category not in result[lexicon]:
                    result[lexicon][category] = []
                rulecode, id1, id2 = rest.split('\t')
                result[lexicon][category].append( (rulecode, id1, id2) )
            
            elif lexicon in( "colors", "metaphors"):
                result[lexicon][category] = rest
                
    return result

loaddatafolders()
data = lexicas()


