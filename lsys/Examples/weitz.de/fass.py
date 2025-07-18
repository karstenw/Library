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
# fill(1,1,0,0.2)


# the actual lsystem parameters
# since L and R move forward in the lib they are replaced here
# with P and Q

axiom = "-P"
rules = {
         "P": "PF+QFQ+FP-F-PFPFP-FQFQ+",
         "Q": "-PFPF+QFQFQ+F+QF-PFP-FQ",
         }

myangle = 90
initialangle = -90
rightangle = -myangle
leftangle = myangle

linelength = 4
depth = 4


# create and draw the lsystem
s = lsys.LindenmayerSystem( axiom, rules,
                            initialangle, rightangle, leftangle,
                            linelength, depth)
s.drawlsystem(inset=0)
