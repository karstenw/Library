# SVG - last updated for NodeBox 1.9.0
# Author: Tom De Smedt <tom@organisms.be>
# Copyright (c) 2006 by Tom De Smedt.
# See also the SVG DOM specification:
# http://www.w3.org/TR/SVG/

import xml.dom.minidom as parser
import re
from nodebox.graphics import RGB, MOVETO

def parse(svg):
       
    dom = parser.parseString(svg)
    return parse_node(dom, [])

def parse_node(node, paths=[]):
    
    """ Recurse the node tree and find drawable tags.
    
    Recures all the children in the node.
    If a child is something we can draw,
    a line, rect, oval or path,
    parse it to a PathElement drawable with drawpath()
    
    """

    if node.hasChildNodes():
        for child in node.childNodes:
            paths = parse_node(child, paths)
    
    if node.nodeType == node.ELEMENT_NODE:

        #try:
        if node.tagName == "line":
            paths.append(parse_line(node))
        if node.tagName == "rect":
            paths.append(parse_rect(node))
        if node.tagName == "ellipse":
            paths.append(parse_oval(node))
        if node.tagName == "polygon":
            paths.append(parse_polygon(node))
        if node.tagName == "polyline":
            paths.append(parse_polygon(node))
        if node.tagName == "path":
            paths.append(parse_path(node))
        #except:
            # Stray points end up here.
        #    pass
    
    return paths

def parse_line(e):
    
    x1 = float(e.getAttribute("x1"))
    y1 = float(e.getAttribute("y1"))
    x2 = float(e.getAttribute("x2"))
    y2 = float(e.getAttribute("y2"))
    p = _ctx.line(x1, y1, x2, y2, draw=False)
    p = add_color_info(e, p)
    return p

def parse_rect(e):
    
    x = float(e.getAttribute("x"))
    y = float(e.getAttribute("y"))
    w = float(e.getAttribute("width"))
    h = float(e.getAttribute("height"))
    p = _ctx.rect(x, y, w, h, draw=False)
    p = add_color_info(e, p)
    return p
            
def parse_oval(e):
    
    x = float(e.getAttribute("cx"))
    y = float(e.getAttribute("cy"))
    w = float(e.getAttribute("rx"))*2
    h = float(e.getAttribute("ry"))*2
    p = _ctx.oval(x-w/2, y-h/2, w, h, draw=False)
    p = add_color_info(e, p)
    return p

def parse_polygon(e):
    
    d = e.getAttribute("points")
    d = d.replace(" ", ",").split(",")
    points = []
    for x in d:
        if x != "": points.append(float(x))
    
    _ctx.autoclosepath()
    if (e.tagName == "polyline") :
        _ctx.autoclosepath(False)
        
    _ctx.beginpath(points[0], points[1])
    for i in range(len(points)/2):
        _ctx.lineto(points[i*2], points[i*2+1])
    p = _ctx.endpath(draw=False)
    p = add_color_info(e, p)
    return p

def parse_path(e):

    d = e.getAttribute("d")
    
    # Divide the path data string into segments.
    # Each segment starts with a path command,
    # usually followed by coordinates.
    segments = []
    i = 0
    for j in range(len(d)):
        commands = ["M", "m", "Z", "z", "L", "l", "H", "h", "V", "v", "C","c", "S", "s"]
        if d[j] in commands:
            segments.append(d[i:j].strip())
            i = j
    segments.append(d[i:].strip())
    segments.remove("")
    
    previous_command = ""
    
    # Path origin (moved by MOVETO).
    x0 = 0
    y0 = 0
    
    # The current point in the path.
    dx = 0
    dy = 0
    
    # The previous second control handle.
    dhx = 0
    dhy = 0
    
    _ctx.autoclosepath(False)
    _ctx.beginpath(0,0)
    for segment in segments:
        
        command = segment[0]

        if command in ["Z", "z"]:
            _ctx.closepath()
        else:
            # The command is a pen move, line or curve.
            # Get the coordinates.
            points = segment[1:].strip()
            points = points.replace("-", ",-")
            points = points.replace(" ", ",")
            points = re.sub(",+", ",", points)
            points = points.strip(",")
            points = [float(i) for i in points.split(",")]
        
        # Absolute MOVETO.
        # Move the current point to the new coordinates.
        if command == "M":
            for i in range(len(points)/2):
                _ctx.moveto(points[i*2], points[i*2+1])
                dx = points[i*2]
                dy = points[i*2+1]
                x0 = dx
                y0 = dy

        # Relative MOVETO.
        # Offset from the current point.
        if command == "m":
            for i in range(len(points)/2):
                _ctx.moveto(dx+points[i*2], dy+points[i*2+1])
                dx += points[i*2]
                dy += points[i*2+1]
                x0 = dx
                y0 = dy
        
        # Absolute LINETO.
        # Draw a line from the current point to the new coordinate.
        if command == "L":
            for i in range(len(points)/2):
                _ctx.lineto(points[i*2], points[i*2+1])
                dx = points[i*2]
                dy = points[i*2+1]

        # Relative LINETO.
        # Offset from the current point.
        if command == "l":
            for i in range(len(points)/2):
                _ctx.lineto(dx+points[i*2], dy+points[i*2+1])
                dx += points[i*2]
                dy += points[i*2+1]

        # Absolute horizontal LINETO.
        # Only the vertical coordinate is supplied.
        if command == "H":
            for i in range(len(points)):
                _ctx.lineto(points[i], dy)
                dx = points[i]

        # Relative horizontal LINETO.
        # Offset from the current point.
        if command == "h":
            for i in range(len(points)):
                _ctx.lineto(dx+points[i], dy)
                dx += points[i]

        # Absolute vertical LINETO.
        # Only the horizontal coordinate is supplied.
        if command == "V":
            for i in range(len(points)):
                _ctx.lineto(dx, points[i])
                dy = points[i]

        # Relative vertical LINETO.
        # Offset from the current point.
        if command == "v":
            for i in range(len(points)):
                _ctx.lineto(dx, dy+points[i])
                dy += points[i]

        # Absolute CURVETO.
        # Draw a bezier with given control handles and destination.
        if command == "C":
            for i in range(len(points)/6):
                _ctx.curveto(points[i*6],   points[i*6+1], 
                             points[i*6+2], points[i*6+3], 
                             points[i*6+4], points[i*6+5])
                dhx = points[i*6+2]
                dhy = points[i*6+3]
                dx = points[i*6+4]
                dy = points[i*6+5]
        
        # Relative CURVETO.
        # Offset from the current point.
        if command == "c":
            for i in range(len(points)/6):
                _ctx.curveto(dx+points[i*6],   dy+points[i*6+1], 
                             dx+points[i*6+2], dy+points[i*6+3], 
                             dx+points[i*6+4], dy+points[i*6+5])
                dhx = dx+points[i*6+2]
                dhy = dy+points[i*6+3]
                dx += points[i*6+4]
                dy += points[i*6+5]

        # Absolute reflexive CURVETO.
        # Only the second control handle is given,
        # the first is the reflexion of the previous handle.
        if command == "S":
            for i in range(len(points)/4):
                if previous_command not in ["C", "c", "S", "s"]:
                    dhx = dx
                    dhy = dy
                else:
                    dhx = dx-dhx
                    dhy = dy-dhy
                _ctx.curveto(dx+dhx, dy+dhy, 
                             points[i*4],   points[i*4+1], 
                             points[i*4+2], points[i*4+3])
                dhx = points[i*4]
                dhy = points[i*4+1]
                dx = points[i*4+2]
                dy = points[i*4+3]
                
        # Relative reflexive CURVETO.
        # Offset from the current point.
        if command == "s":
            for i in range(len(points)/4):
                if previous_command not in ["C", "c", "S", "s"]:
                    dhx = dx
                    dhy = dy
                else:
                    dhx = dx-dhx
                    dhy = dy-dhy
                _ctx.curveto(dx+dhx, dy+dhy, 
                             dx+points[i*4],   dy+points[i*4+1], 
                             dx+points[i*4+2], dy+points[i*4+3])
                dhx = dx+points[i*4]
                dhy = dy+points[i*4+1]
                dx += points[i*4+2]
                dy += points[i*4+3]

        previous_command = command
        
    p = _ctx.endpath(draw=False)
    p = add_transform_matrix(e, p)
    p = add_color_info(e, p)    
    return p

def add_transform_matrix(e, path):
    
    """ Transform the path according to a defined matrix.
    
    Attempts to extract a transform="matrix()" attribute.
    Transforms the path according to this matrix.
    
    """
    
    matrix = e.getAttribute("transform")
    if matrix.startswith("matrix("):
        
        matrix = matrix.replace("matrix(", "").rstrip(")")
        matrix = matrix.split(",")
        matrix = [float(v) for v in matrix]
    
        from nodebox.graphics import Transform
        t = Transform()
        t._set_matrix(matrix)
        path = t.transformBezierPath(path)
        
    return path

def add_color_info(e, path):
    
    """ Expand the path with color information.
    
    Attempts to extract fill and stroke colors
    from the element and adds it to path attributes.
    
    """
    
    _ctx.colormode(RGB, 1.0)
    
    def _color(hex, alpha=1.0):
        if hex == "none": return None
        n = int(hex[1:],16)
        r = (n>>16)&0xff
        g = (n>>8)&0xff
        b = n&0xff
        return _ctx.color(r/255.0, g/255.0, b/255.0, alpha)

    path.fill = None
    path.stroke = None
    path.strokewidth = 0

    # See if we can find an opacity attribute,
    # which is the color's alpha.
    alpha = e.getAttribute("opacity")
    if alpha == "":
        alpha = 1.0
    else:
        alpha = float(alpha)
    
    # Colors stored as fill="" or stroke="" attributes.
    try: path.fill = _color(e.getAttribute("fill"), alpha)
    except: pass
    try: path.stroke = _color(e.getAttribute("stroke"), alpha)
    except: pass
    try: path.strokewidth = float(e.getAttribute("stroke-width"))
    except: pass
    
    # Colors stored as a CSS style attribute, for example:
    # style="fill:#ff6600;stroke:#ffe600;stroke-width:0.06742057"
    style = e.getAttribute("style").split(";")
    for s in style:
        try:
            if s.startswith("fill:"):
                path.fill = _color(s.replace("fill:", ""))
            if s.startswith("stroke:"):
                path.stroke = _color(s.replace("stroke:", ""))
            if s.startswith("stroke-width:"):
                path.strokewidth = float(s.replace("stroke-width:", ""))
        except:
            pass
    
    # A path with beginning and ending coordinate
    # at the same location is considered closed.
    # Unless it contains a MOVETO somewhere in the middle.
    path.closed = False
    if path[0].x == path[len(path)-1].x and \
       path[0].y == path[len(path)-1].y: 
        path.closed = True
    for i in range(1,len(path)-1):
        if path[i].cmd == MOVETO:
            path.closed = False
        
    return path