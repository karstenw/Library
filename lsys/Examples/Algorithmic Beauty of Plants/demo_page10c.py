size(320, 320)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 10 image c

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
rules = {"F":"FF-F+F-F-FF"}

ang = 90
linelength = 12
depth = 3


s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)
s.generate()
r = s.walk(200, 50, -90, drawit=True)

b = s.boundingBox
print b
