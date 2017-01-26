# -*- coding: utf-8 -*-


import math
sin = math.sin
cos = math.cos

import pdb

import pprint
pp = pprint.pprint

class DrawingState(object):
    """Represent the drawing state for a Lindenmayer system.
    
    pen - state of the pen True/False for down/up
    halfcoordinates - place coordinates on x.5 and y.5 
    """

    def __init__(self, x, y, heading, pen):
        
        self._x = x
        self._y = y
        self._heading = heading
        self.pen = pen
        self.halfcoordinates = True

        if x == int(x):
            if self.halfcoordinates:
                self._x, self._y = self.cocoaOffset(x, y)

        self.stack = []

        # for finding the bounding box
        self._minX = x + 100
        self._maxX = x - 100

        self._minY = y + 100
        self._maxY = y - 100
        
        self._customLine = None
        self._customMove = None

    def push(self):
        item = (self._x, self._y, self._heading, self.pen)
        self.stack.append( item )

    def pop(self):
        if len(self.stack) == 0:
            print "EMPTY STACK ERROR"
            pdb.set_trace()
            print
        
        item = self.stack.pop()
        self._x, self._y, self._heading, self.pen = item
        return self.move(0)

    def heading(self):
        return self._heading
    
    def setHeading(self, deg):
        self._heading += deg
        self._heading %= 360.0
        return self._heading

    def cocoaOffset(self, x, y):
        """One pixel lines look better if placed on half coordinates in cocoa."""
        return ( x + 0.5, y + 0.5 )

    def move(self, steps):
        self.pen = False
        return self.calcmove( steps )

    def draw(self, steps):
        self.pen = True
        return self.calcmove( steps )

    def calcmove(self, steps):
        """Move the pen by steps. Draw a line if pen is down.
        
        returns a tuple( newx, newy, pendown )
        """
        oldx, oldy = self._x, self._y

        rad = self._heading * 0.0174532925199433

        x = oldx + (cos( rad ) * steps)
        y = oldy + (sin( rad ) * steps)

        self._x = x
        self._y = y
        self.adaptBoundingBox()
        
        if self.pen:
            if self._customLine:
                self._customLine( x, y )

        else:
            if self._customMove:
                self._customMove( x, y )
        
        x = int( x * 10 ) / 10.0
        y = int( y * 10 ) / 10.0
        return (x, y, self.pen)


    def adaptBoundingBox(self):
        if self._x > self._maxX:
            self._maxX = self._x
        if self._x < self._minX:
            self._minX = self._x
        if self._y > self._maxY:
            self._maxY = self._y
        if self._y < self._minY:
            self._minY = self._y


    def boundingBox(self):
        # top left bottom right
        return ( self._minY, self._minX, self._maxY, self._maxX )

        # old return value
        #       ( (self._minX, self._maxX),
        #         (self._minY, self._maxY))


class LindenmayerSystem(object):
    def __init__(self, axiom, rules, phi, rightAngle, leftAngle, movelength, depth):
        self.axiom = axiom
        self.rules = rules
        self.phi = phi
        self.rightAngle = rightAngle
        self.leftAngle = leftAngle
        self.movelength = movelength
        self.depth = depth
        self.symbols = list( self.axiom )

        self.currentPoint = (0,0)
        self.size = (1000,1000)
        self.boundingBox = ()

    def demo(self):
        self.axiom = "F+F+F+F"
        self.rules = {"F": "FF+F-F+F+FF"}
        self.currentPoint = (0,0)
        self.size = (1000,1000)
        self.phi = 90
        self.rightAngle = self.phi
        self.leftAngle = -self.phi
        self.movelength = 8
        self.depth = 1
        self.symbols = list( self.axiom )

    
    def generate(self):
        """Set symbols to final generation."""
        self.reset()
        for i in range(1, self.depth+1):
            self.substitute()

    def reset( self ):
        self.symbols = list( self.axiom )

    def asString(self):
        return "".join( self.symbols )

    def substitute(self):
        """applies one generation of lsys rules to symbols"""

        rules = self.rules
        result = []

        for t in self.symbols:
            for c in t:
                s = c
                t = rules.get(c, c)
                # print s,t
                result.extend( t )
        self.symbols = result


    #####

    def walk(self, x, y, heading, drawit=True):
        """Walk the symbols list.
        
        If drawit == True, lines are drawn in the current style.
        
        If drawit == False, the drawing commands are collected and returned.
            The bounding box is set and could be used for adjustments.
        """
        penup = False
        pendown = True

        ds = DrawingState(x, y, heading, penup)

        result = []

        if drawit:
            #_ctx.strokewidth( 1.0 )
            #_ctx.stroke( 0 )
            #_ctx.nofill()
            _ctx.autoclosepath(False)
            p = _ctx.beginpath()
            _ctx.moveto(ds._x, ds._y)
        
        for s in self.symbols:
            x = self.executeRule( ds, s )
            if type(x) in (tuple,):
                if drawit:
                    x2,y2,pen = x
                    if pen:
                        _ctx.lineto(x2,y2)
                    else:
                        _ctx.moveto(x2,y2)
                else:
                    result.append( x )

        if drawit:
            p = _ctx.endpath()
            # _ctx.drawpath( p )
        self.boundingBox = ds.boundingBox()
        return result

    def adjustToBoundingBox( self, bbox, inset=0):
        # bbox is top left bottom right
        t, l, b, r = bbox
        offset = -l + inset, -t + inset
        canvassize = int(r - l) + 2 * inset, int(b - t) + 2 * inset
        return offset, canvassize


    def executeRule(self, ds, rule):
        """The rules are:
            F,L,R,G,f: draw
            +: turn rightangle degrees
            -: turn leftangle degrees
            [: push state
            ]: pop state
        """

        # pdb.set_trace()

        if rule == 'F':
            return ds.draw( self.movelength )
        elif rule == 'L':
            return ds.draw( self.movelength )
        elif rule == 'R':
            return ds.draw( self.movelength )
        elif rule == 'G':
            return ds.draw( self.movelength )
        elif rule == "f":
            return ds.move( self.movelength )
        elif rule in "FLRG":
            return ds.draw( self.movelength )
        elif rule == '+':
            return ds.setHeading( self.rightAngle )
        elif rule == '-':
            return ds.setHeading( self.leftAngle )
        elif rule == "|":
            return ds.setHeading( 180 )
        elif rule == "[":
            return ds.push()
        elif rule == "]":
             return ds.pop()
        return rule


    def drawlsystem(self, inset=1):
        # apply the rules
        self.generate()

        # calculate the drawing size
        self.walk(0, 0, 0, drawit=False)

        # get the bounding box
        bbox = self.boundingBox

        # calculate offset and canvas size
        offset, canvassize = self.adjustToBoundingBox( bbox, inset=inset)

        W, H = canvassize
        x, y = offset

        # now we know that width = W, height = H and the offset

        # set canvas size
        _ctx.size( W, H )
        #_ctx.background( None )

        # apply offset
        _ctx.translate(x-0.5, y-0.5)

        # finally draw it
        self.walk(0, 0, 0, drawit=True)




if 0:
    s = LindenmayerSystem("F+F+F+F",
                          {"F": "FF+F-F+F+FF"},
                          90, 90, -90,
                          8, 3)

    s.substitute()

    pp(s.walk())
    pp(s.boundingBox)
