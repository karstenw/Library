# Author: Tom De Smedt <tomdesmedt@trapdoor.be>
# Manual: http://nodebox.net/code/index.php/Explode
# Copyright (c) 2004 by Tom De Smedt.
# Usage is free for non-commercial use:
# refer to the "Use" section on http://nodebox.net/code

from nodebox.graphics import CORNER, CENTER

def node(leaves, x, y, angle, vpad=1.0):
    
    """Draws a node in the network
    
    A node is a central oval with branching leaves.
    Each leaf in the list is a string with its description.
    
    """
    
    size = _ctx.fontsize()
    _ctx.fontsize(size)
    
    _ctx.oval(x-size*0.25, y-size*0.25, size*0.5, size*0.5)
    
    #Defines a number of degrees to rotate
    #each leaf branch. Leaves branch in relation
    #to the node's branch, defined by the given angle.
    ri = 360.0 / len(leaves)
    ri = min(20, ri)
    r0 = angle - ri * (len(leaves)-1) * 0.5

    w = size * 5

    for leaf in leaves:
        
        _ctx.push()
        _ctx.transform(CORNER)
        _ctx.translate(x,y)
        _ctx.rotate(r0)
        _ctx.line(0,0,w,0)
        #Depending on which font is used,
        #the leaf text may (will) not align nicely
        #to the middle of the leaf branch.
        #vpad (vertical padding) can be used to
        #correct this.
        _ctx.text(leaf, w+_ctx.textwidth(" "), size/3)
        _ctx.pop()
        
        r0 += ri
        
def explode(name, nodes, x, y, max=50, vpad=1.0, shuffleNodes=1):
    
    """Draws a central point named with given name,
    and branching nodes from that point.
    
    """
    
    size = _ctx.fontsize()
    _ctx.lineheight(1.2)
    
    if _ctx.stroke() == None: _ctx.stroke(_ctx.fill())
    if _ctx.strokewidth() == 0: _ctx.strokewidth(0.5)
    
    #To avoid a clutter of node leaves,
    #limit the number of nodes and shuffle them,
    #so there is a random chance of nodes with
    #a different amount of leaves appearing next
    #to each other.
    #This makes for a harmonious tree.
    nodes = nodes[:max]
    if shuffleNodes:
        from random import shuffle
        shuffle(nodes)
    
    #Define a minimum number of degrees
    #to rotate each branching node, based
    #on the number of nodes.
    ri = 360.0 / len(nodes)
    ri = min(60, ri)
    r0 = 0
        
    for leaves in nodes:
        
        #Node branches are longer of there are more nodes.
        #This is the inner radius.
        #Nodes that have many leaves branches even further.
        #This is the outer radius.
        inside = size * len(nodes) * 0.1
        outside = size * min(7, len(leaves)) * 8.5
        w = inside + outside
        
        _ctx.push()
        _ctx.transform(CORNER)
        _ctx.translate(x,y)
        _ctx.rotate(r0)
        _ctx.line(0,0,w,0)
        node(leaves, w, 0, 0, vpad)
        _ctx.pop()
        
        r0 += ri
        
    f = _ctx.fill()
    _ctx.fill(1)
    _ctx.oval(x-size*1.5, y-size*1.5, size*3, size*3)
    _ctx.fill(f)
    
    _ctx.fontsize(size*2)
    _ctx.align(CENTER)
    _ctx.text(name, x-size*10, y+size/2, size*20)
    _ctx.fontsize(size)