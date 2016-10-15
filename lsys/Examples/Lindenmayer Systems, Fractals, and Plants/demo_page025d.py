size(300, 450)

# From the book
# "Lindenmayer Systems, Fractals, and Plants"
# 
# http://algorithmicbotany.org/papers/#lsfp

try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
reload(lsys)


strokewidth( 1.0 )
stroke( 0 )
nofill()

import pprint
pp = pprint.pprint

axiom = "F"
rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
angle = 22.5
linelength = 8
depth = 4


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.generate()
r = s.walk(100, 449, -90, drawit=1)

b = s.boundingBox
print b
