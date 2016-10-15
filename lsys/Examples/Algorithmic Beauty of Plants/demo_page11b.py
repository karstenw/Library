size(256, 256)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 10 image f

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

axiom = "R"
rules = {"L": "R+L+R",
         "R": "L-R-L"}

ang = 60
linelength = 4
depth = 6


s = lsys.LindenmayerSystem( axiom, rules, ang, ang, -ang, linelength, depth)
s.generate()
r = s.walk(255, 255, 180, drawit=True)

b = s.boundingBox
print b
