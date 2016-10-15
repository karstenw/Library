size(200, 200)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 10 image e

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

axiom = "F-F-F-F"
rules = {"F":"F-FF--F-F"}

ang = 90
linelength = 2
depth = 5


s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)
s.generate()
r = s.walk(165, 91, 0, drawit=True)

b = s.boundingBox
print b
