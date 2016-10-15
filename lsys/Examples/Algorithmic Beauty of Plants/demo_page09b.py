size(900, 900)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 9

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

axiom = "-F"
rules = {"F":"F+F-F-F+F"}

ang = 90
linelength = 8
depth = 4


s = lsys.LindenmayerSystem( axiom, rules, ang, ang, -ang, linelength, depth)
s.generate()
r = s.walk(700, 380, -90, drawit=True)

b = s.boundingBox
print b
