size(240, 240)

# all examples translated from 
# 
# http://weitz.de/files/Lindenmayer.zip,


# import library
try: 
    lsys = ximport("lsys")
except:
    lsys = ximport("__init__")
# reload( lsys )

# color and line attributes
strokewidth( 0.5 )
stroke( 0 )

nofill()

axiom = "FB"

rules = {
         "A": "FBFA+HFA+FB-FA",
         "B": "FB+FA-FB-JFBFA",
         "H": "-",
         "J": "+",
         "F": "",
        }

myangle = 90
initialangle = 0
rightangle = -myangle
leftangle = myangle

linelength = 4
depth = 5


# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
