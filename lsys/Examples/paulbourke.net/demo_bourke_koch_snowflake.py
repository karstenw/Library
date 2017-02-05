# From  the website:
#
# see http://paulbourke.net/fractals/vonkoch_snowflake/

try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
reload(lsys)

background( None )

strokewidth( 1 )
stroke( 0 )
# nofill()
fill(1,1,0,0.1)

import pprint
pp = pprint.pprint

axiom = "F++F++F"
rules = {"F": "F-F++F-F"}
myangle = 60
linelength = 8
depth = 4


s = lsys.LindenmayerSystem( axiom, rules, myangle, myangle, -myangle, linelength, depth)
s.drawlsystem(inset=5)