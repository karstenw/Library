try:
    beziereditor = ximport("beziereditor")
except:
    beziereditor = ximport("__init__")
    reload(beziereditor)

speed(100)
size(800, 800)

fonts = fontnames()

f = choice( fonts )
print f

def setup():
    
    global editor

    # Initialize the editor with a path
    # constructed from a character.
    fontsize(600)
    p = textpath("a", 80, 600, font=f)
    editor = beziereditor.start(p, filename="path")

def draw():
    
    global editor
    editor.draw()