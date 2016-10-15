size(500, 500)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 10 image d

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
rules = {"F":"FF-F--F-F"}

ang = 90
linelength = 6
depth = 4


s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)
s.generate()
r = s.walk(7, 7, 0, drawit=True)

b = s.boundingBox
print b
