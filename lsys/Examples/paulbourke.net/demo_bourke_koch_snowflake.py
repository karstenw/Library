size(1000, 1200)

# From  the website:
#
# see http://paulbourke.net/fractals/vonkoch_snowflake/

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

axiom = "F++F++F"
rules = {"F": "F-F++F-F"}
angle = 60
linelength = 4
depth = 5


s = lsys.LindenmayerSystem( axiom, rules, angle, angle, -angle, linelength, depth)
s.generate()
r = s.walk(1, 300, 0, drawit=True)

b = s.boundingBox
print b
