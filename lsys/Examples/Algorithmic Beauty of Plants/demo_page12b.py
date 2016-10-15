size(256, 256)

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

axiom = "-R"
rules = {"L": ("LL-R-R+L+L-R-RL+"
               "R+LLR-L+R+LL+"
               "R-LR-R-L+L+RR-"),
         "R": ("+LL-R-R+L+LR+L-"
               "RR-L-R+LRR-L-"
               "RL+L+R-R-L+L+RR")}

ang = 90
linelength = 10
depth = 2


s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)
s.generate()
r = s.walk(1, 255, -90, drawit=True)

b = s.boundingBox
print b
