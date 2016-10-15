size(1200, 1200)

# From the website
#
# http://bl.ocks.org/nitaku/8b9e134ca8bae13bb470

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
axiom = "-Y"
rules = {"X": "XF",
         "Y": "Y+XF+XF"}

ang = 90
linelength = 6
depth = 72


s = lsys.LindenmayerSystem( axiom, rules, ang, ang, -ang, linelength, depth)
s.generate()
r = s.walk(600, 600, 0, drawit=True)

b = s.boundingBox
print b
