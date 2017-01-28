## LSYS Library ##

This is a Lindenmayer library written from scratch.

Why?

Because it's fun!


The recognized symbols are:

+ F,L,R,G - Move forward one steplength drawing a line

+ f - Move forward one steplength

+ +,- turn right- or left angle degrees

+ | turn 180 degrees

+ [,] push / pop the graphics state

Remember: You can use any one character as a symbol in replacement rules. Only "FLRGf+-|[]" have actions associated with them.


## Usage ##

```Python

s = lsys.LindenmayerSystem( axiom, rulesdict, initialangle, rightangle, leftangle, steplength, depth)

s.drawlsystem(inset=0)

```
