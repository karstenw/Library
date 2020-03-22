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
# fill(1,1,0,0.2)


# the actual lsystem parameters
# since L and R move forward in the lib they are replaced here
# with P and Q
axiom = "-FR"
rules = {
         "L": "FLFL-FR-FR+FL+FL-FR-FRFL+FR+FLFLFR-FL+FR+FLFL+FR-FLFR-FR-FL+FL+FRFR-",
         "R": "+FLFL-FR-FR+FL+FLFR+FL-FRFR-FL-FR+FLFRFR-FL-FRFL+FL+FR-FR-FL+FL+FRFR",
         "F": ""
         }

myangle = 90
initialangle = 90
rightangle = myangle
leftangle = -myangle

linelength = 2
depth = 3


# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
