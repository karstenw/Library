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
        return ( x + 0.5, y + 0.5 )

    def move(self, steps):
        self.pen = False
        return self.calcmove( steps )

    def draw(self, steps):
        self.pen = True
        return self.calcmove( steps )

    def calcmove(self, steps):
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
        return ( (self._minX, self._maxX),
                 (self._minY, self._maxY))


class LindenmayerSystem(object):
    def __init__(self, axiom, rules,phi, r, l, m, d):
        self.axiom = axiom
        self.rules = rules
        self.phi = phi
        self.rightAngle = r
        self.leftAngle = l
        self.movelength = m
        self.depth = d
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
        """applies lsys rules to symbols"""

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
    
    def mylineto(self, x2, y2):
        _ctx.lineto(x2,y2)
    
    def mymoveto(self, x2, y2):
        _ctx.moveto(x2,y2)

    def walk(self, x, y, h, drawit=True): # , linetoproc=None, movetoproc=None):

        ds = DrawingState(x,y,h, False)

        result = []

        if drawit:
            _ctx.strokewidth( 1.0 )
            _ctx.stroke( 0 )
            _ctx.nofill()
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
if 0:
    s = LindenmayerSystem("F+F+F+F",
                          {"F": "FF+F-F+F+FF"},
                          90, 90, -90,
                          8, 3)

    s.substitute()

    pp(s.walk())
    pp(s.boundingBox)