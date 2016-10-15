

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

axiom = "Y"
rules = {"Y": "YFX[+Y][-Y]",
         "X":  "X[-FFF][+FFF]FX"}
angle = 25.7
linelength = 4
depth = 6


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.generate()
r = s.walk(500, 999, -90, drawit=1)

b = s.boundingBox
print b
