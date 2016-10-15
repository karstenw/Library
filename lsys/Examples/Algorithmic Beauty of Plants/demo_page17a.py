size(240, 240)

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

# since L and R move forward in the lib they are replaced here
# with P and Q
axiom = "-P"
rules = {"P": "PF+QFQ+FP-F-PFPFP-FQFQ+",
         "Q": "-PFPF+QFQFQ+F+QF-PFP-FQ"}

ang = 90
linelength = 8
depth = 3


s = lsys.LindenmayerSystem( axiom, rules, ang, -ang, ang, linelength, depth)
s.generate()
r = s.walk(10, 230, -90, drawit=True)

b = s.boundingBox
print b
