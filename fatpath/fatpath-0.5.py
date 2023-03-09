# FATPATH 0.5 -- Frederik De Bleser
# Released under the MIT License.
#
# Fatpath does mathematics on path points. The formula is as follows:
#
#   p1 + (p2 - p1) * fatness
#
# Run this script and play with the variables. They are the following:
#  - font1: The PostScript name of the (regular) font
#  - font2: The PostScript name of the (bold) font
#  - message: The message to display
#  - fatness: The multiplying factor
#  - randomness: An extra random amount added to each point
# Confirm every change to a field by pressing <enter>.
#
# IMPORANT: Fatpath is rather dumb and doesn't do any interpolation
# at all. That means that paths have to match *exactly* between
# two points. This means you can only use fonts of the same family, and
# even then, there is no guarantee that letters match. Letters with curves
# are especially troublesome. Push the letters_that_work button to find
# out which letters you can use for the given fonts. (After pushing the button,
# you might have to set the fonts again. This is a NodeBox bug.)
#
# Here are some fonts that have reasonable success:
#  - HelveticaNeue and HelveticaNeue-Bold
#  - LucidaGrande and LucidaGrande-Bold
#
# The PostScript name of a font can be looked up in the Font Book application.
# Select a font you like and go to Preview > Show Font Info. The PostScript name
# is the first field.

var("font1", TEXT, "HelveticaNeue")
var("font2", TEXT, "HelveticaNeue-Bold")
var("message", TEXT, "FAT!")
var("textsize", NUMBER, 150, 10, 300)
var("fatness", NUMBER, 3.3, -10.0, 10.0)
var("randomness", NUMBER, 0.0, 0.0, 40.0)
var("points", BOOLEAN, False)
var("letters_that_work", BUTTON)

    
class PathMathError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

size(700, 500)

def op_add(a, b):
    return a + b + random(-randomness, randomness)

def op_sub(a, b):
    return a - b

def op_mul(a, b):
    r = -0.4
    return a * b # + random(-r, r)
    
def op_div(a, b):
    return a / b

def pe_op(el1, el2, op):
    if el1.cmd != el2.cmd:
        raise PathMathError("PathCommand %s != %s" % (el1.cmd, el2.cmd))
    if el1.cmd == CLOSE:
        return PathElement(CLOSE)
    elif el1.cmd == MOVETO or el1.cmd == LINETO:        
        x = op(el1.x, el2.x)
        y = op(el1.y, el2.y)
        return PathElement(el1.cmd, [[x, y]])
    elif el1.cmd == CURVETO:
        x = op(el1.x, el2.x)
        y = op(el1.y, el2.y)
        ctrl1x = op(el1.ctrl1.x, el2.ctrl1.x)
        ctrl1y = op(el1.ctrl1.y, el2.ctrl1.y)
        ctrl2x = op(el1.ctrl2.x, el2.ctrl2.x)
        ctrl2y = op(el1.ctrl2.y, el2.ctrl2.y)    
        return PathElement(el1.cmd, ((ctrl1x, ctrl1y), (ctrl2x, ctrl2y), (x, y)))
    else:
        raise "aarh"

def pe_sop(el1, n, op):
    if el1.cmd == CLOSE:
        return PathElement(CLOSE)
    elif el1.cmd == MOVETO or el1.cmd == LINETO:        
        x = op(el1.x, n)
        y = op(el1.y, n)
        return PathElement(el1.cmd, [[x, y]])
    elif el1.cmd == CURVETO:
        x = op(el1.x, n)
        y = op(el1.y, n)
        ctrl1x = op(el1.ctrl1.x, n)
        ctrl1y = op(el1.ctrl1.y, n)
        ctrl2x = op(el1.ctrl2.x, n)
        ctrl2y = op(el1.ctrl2.y, n)
        return PathElement(el1.cmd, ((ctrl1x, ctrl1y), (ctrl2x, ctrl2y), (x, y)))
    else:
        raise "Unknown command %s" % el1.cmd

def pe_gop(el1, el2, op):
    if isinstance(el2, int) or isinstance(el2, float):
        return pe_sop(el1, el2, op)
    else:
        return pe_op(el1, el2, op)

def pe_add(el1, el2):
    return pe_gop(el1, el2, op_add)
    
def pe_sub(el1, el2):
    return pe_gop(el1, el2, op_sub)

def pe_div(el1, el2):
    #print "pe_div", el1, el2, op_div
    return pe_gop(el1, el2, op_div)
    
def pe_mul(el1, n):
    return pe_gop(el1, n, op_mul)

def subtractpath(p1, p2):
    path = BezierPath()
    for i in range(p1len):
        pe = subtract(p1[i], p2[i])
        path.append(pe)
    return path


def path_assert_len(p1, p2):
    p1len = len(p1)
    p2len = len(p2)
    if p1len != p2len:
        raise PathMathError("Length of path %s != %s" % (p1len, p2len))


def path_op(p1, p2, op):
    #print "path_op", p1, p2, op
    path_assert_len(p1, p2)
    path = BezierPath()
    for i in range(len(p1)):
        pe = op(p1[i], p2[i])
        path.append(pe)
    return path
    
# single op
def path_sop(p1, n, op):
    path = BezierPath()
    for i in range(len(p1)):
        pe = op(p1[i], n)
        path.append(pe)
    return path
    
# generic op
def path_gop(p1, p2, op):
    if isinstance(p2, int) or isinstance(p2, float):
        return path_sop(p1, p2, op)
    else:
        return path_op(p1, p2, op)        

def path_add(p1, p2):
    return path_gop(p1, p2, pe_add)

def path_sub(p1, p2):
    return path_gop(p1, p2, pe_sub)

def path_mul(p1, p2):
    return path_gop(p1, p2, pe_mul)

def path_div(p1, p2):
    return path_gop(p1, p2, pe_div)
    
def peprint(pe):
    if pe.cmd == MOVETO:
        print( "<PathElement moveto %s,%s>" % (pe.x, pe.y) )
    elif pe.cmd == LINETO:
        print( "<PathElement lineto %s,%s>" % (pe.x, pe.y) )
    elif pe.cmd == CURVETO:
        print( "<PathElement curveto %s,%s %s,%s %s,%s >" % (pe.x, pe.y, pe.ctrl1.x, pe.ctrl1.y, pe.ctrl2.x, pe.ctrl2.y) )
    elif pe.cmd == CLOSE:
        print( "<PathElement close>" )

def drawpoints(path):    
    fill(1, 0, 0)
    for pe in path:
        if pe.cmd != CLOSE:
            oval(pe.x-2, pe.y-2, 4, 4)
    fill(0)

deltas = []

def err_msg(msg):
    msg = str(msg)
    fill(1,0,0)
    font("Helvetica-Bold", 24)
    text(msg, 10, 400)
    
def fatpath(p1, p2, factor=2.0):
    return path_add(p1, path_mul(path_sub(p2, p1), factor))
                 
def path_draw(p, x, y, points=True):
    push()
    translate(x, y)
    drawpath(p)
    if points:
        drawpoints(p)
    pop()
    
def main():
    try:
        font(font1, textsize)
        path1 = textpath(message, 0, 150)
        font(font2, textsize)
        path2 = textpath(message, 0, 150)

        path_draw(path1, 0, 0, points)
        path_draw(path2, 0, 150, points)
        fp = fatpath(path1, path2, fatness)
        path_draw(fp, 0, 300, points)
    except Exception as e:
        err_msg(str(e))

def path_commands_equal(p1, p2):
    for i in range(len(p1)):
        pe1 = p1[i]
        pe2 = p2[i]
        if pe1.cmd != pe2.cmd:
            return False
    return True

def letters_that_work():
    """Displays a list of letters that work"""
    import string
    print()
    print( "Letters that work with %s and %s:" % (font1, font2) )
    print( "    ", )
    cnt = 0
    for letter in string.printable:
        font(font1, 150)
        p1 = textpath(letter, 0, 0)
        font(font2, 150)
        p2 = textpath(letter, 0, 0)
        if len(p1) == len(p2):
            if path_commands_equal(p1, p2):
                print( letter, )
                cnt += 1
                if cnt > 20:
                    print() 
                    print( "    ", )
                    cnt = 0
    print()
    print()
    main()

main()
