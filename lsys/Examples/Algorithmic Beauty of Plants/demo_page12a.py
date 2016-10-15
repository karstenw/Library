size(512, 512)

# From the book
# "Algorithmic Beauty of Plants"
# 
# http://algorithmicbotany.org/papers/#abop
#
# page 12 image a

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

axiom = "L"
rules = {"L": "L+R++R-L--LL-R+",
         "R": "-L+RR++R+L--L-R"}

ang = 60
linelength = 8
depth = 4


s = lsys.LindenmayerSystem( axiom, rules, ang, ang, -ang, linelength, depth)
s.generate()
r = s.walk(300, 10, 0, drawit=True)

b = s.boundingBox
print b
