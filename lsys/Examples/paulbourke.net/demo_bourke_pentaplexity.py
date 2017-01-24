size(4800, 4800)

# From  the website:
#
# http://paulbourke.net/fractals/pentaplexity/

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

axiom = "F++F++F++F++F"
rules = {"F": "F++F++F|F-F++F"}
angle = 36
linelength = 24
depth = 5


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.generate()
r = s.walk(910, 1, 0, drawit=True)

b = s.boundingBox
print b