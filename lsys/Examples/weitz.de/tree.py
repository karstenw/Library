size(240, 240)

# all examples translated from 
# 
# http://weitz.de/files/Lindenmayer.zip,


# import library
try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
reload(lsys)

# color and line attributes
strokewidth( 0.5 )
stroke( 0 )

nofill()

# the actual lsystem parameters
# since L and R move forward in the lib they are replaced here
# with P and Q

axiom = "L"
rules = {
         "L": "LL",
         "G": "L[G]G",
         "F": ""
         }

myangle = 30
initialangle = 90
rightangle = myangle
leftangle = -myangle

linelength = 20
depth = 5


# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
