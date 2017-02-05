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
# fill(1, 1, 0, 0.3)

import pprint
pp = pprint.pprint

axiom = "F++F++F++F++F"
rules = {"F": "F++F++F|F-F++F"}
angle = 36
linelength = 12
depth = 4


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.drawlsystem(inset=0)