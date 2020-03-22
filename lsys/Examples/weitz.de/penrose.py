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

axiom = "+WF--XF---YF--ZF"

rules = {
         "W": "YF++ZF----XF[-YF----WF]++",
         "X": "+YF--ZF[---WF--XF]+",
         "Y": "-WF++XF[+++YF++ZF]-",
         "Z": "--YF++++WF[+ZF++++XF]--XF",
         "F": "",
         }

myangle = 36
initialangle = 0
rightangle = -myangle
leftangle = myangle

linelength = 32
depth = 4


# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
