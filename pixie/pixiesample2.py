
size(800, 800)

# Import the library
try:
    # This is the statement you normally use.
    pixie = ximport("pixie")
except:
    # But since this example is "inside" the library
    # we may need to try something different when
    # the library is not located in /Application Support
    pixie = ximport("__init__")

# Set the amount of errors, and draw a paragraph
pixie.distraction(0.5)


for x, y in grid(8, 8, 80, 80):
    pixie.sprite(100+x, 100+y)