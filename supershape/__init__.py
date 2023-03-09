# SUPERSHAPE - last updated for NodeBox 1.9.4
# Author: Frederik De Bleser <frederik@pandora.be>
# Copyright (c) 2006 by Frederik De Bleser.
# See LICENSE.txt for details.

# The superformula was published by Johan Gielis,
# you may use it in NodeBox for non-commercial purposes.

from __future__ import print_function

from math import pi, sin, cos, pow



TWOPI = pi * 2

try:
    
    # Attempt to import the C library
    # for faster performance.
    from . cSuperformula import supercalc
    print("FAST Superformula")

except Exception as err:
    print("Failed loading shared object for Superformula")
    print(err)
    # Else, use the native python
    # calculation of supershapes.
    def supercalc(m, n1, n2, n3, phi):
        a = 1.0
        b = 1.0
    
        t1 = cos(m * phi / 4) / a
        t1 = abs(t1)
        t1 = pow(t1, n2)
    
        t2 = sin(m * phi / 4) / b
        t2 = abs(t2)
        if t2 == 0.0:
            t2 = 0.001
        if 0:
            print( "t2:", t2 )
            print( "n1:", n1 )
            print( "n3:", n3 )
        t2 = pow(t2, n3)
    
        r = pow(t1 + t2, 1 / n1)
        if abs(r) == 0:
            return (0,0)
        else:
            r = 1 / r
            return (r * cos(phi), r * sin(phi))
    print("SLOW")


def path(x, y, w, h, m, n1, n2, n3, points=1000, percentage=1.0, range_=TWOPI):
    first = True
    for i in range(points):
        if i > points*percentage: 
            continue
        phi = i * range_ / points
        dx, dy = supercalc(m, n1, n2, n3, phi)
        dx = (dx * w) + x
        dy = (dy * h) + y
        if first:
            _ctx.beginpath(dx, dy)
            first = False
        else:
            _ctx.lineto(dx, dy)
    return _ctx.endpath(draw=False)
    
def transform(path, m, n1, n2, n3, points=100, range_=TWOPI):
    first = True
    for i in range(points):
        pt = path.point(float(i)/points)
        phi = i * range_ / points
        dx, dy = supercalc(m, n1, n2, n3, phi)
        if first:
            _ctx.beginpath(pt.x+dx, pt.y+dy)
            first = False
        else:
            _ctx.lineto(pt.x+dx, pt.y+dy)
    return _ctx.endpath(draw=False)

#import pprint
#pprint.pprint( globals() )
