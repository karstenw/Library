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

axiom = "F"

rules = {
         "F": "F[+F[+F][-F]F][-F[+F][-F]F]F[+F][-F]F",
        }

myangle = 30
initialangle = -90
rightangle = -myangle
leftangle = myangle

linelength = 8
depth = 3


# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
