

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
rules = {"X": "F-[[X]+X]+F[+FX]-X",
         "F":  "FF"}
angle = 22.5
linelength = 3
depth = 7


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.generate()
r = s.walk(500, 999, -90, drawit=1)

b = s.boundingBox
print b
