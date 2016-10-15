size(512, 512)

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

axiom = "X"
rules = {"X": "F[+X]F[-X]+X",
         "F": "FF"}
angle = 20
linelength = 2
depth = 7


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.generate()
r = s.walk(256, 511, -90, drawit=1)

b = s.boundingBox
print b
