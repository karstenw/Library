size(600,360)
speed(100)

try: 
    coreimage = ximport("coreimage")
except:
    coreimage = ximport("__init__")
    reload(coreimage)
img = ""
def setup():
    
    global img
    img = choice(list(imagefiles("/Library/Desktop Pictures", True)))

def draw():

    global img
    canvas = coreimage.canvas(600,360)
    canvas.append(color(0))
    l = canvas.append(img)
    
    d = FRAME
    l.filter("bumpdistortion", radius=350-d, scale=-4+d*0.01)
    l.filter("bumpdistortion", radius=250-d, scale=-4+d*0.01, dy=-d+100)
    l.scale(1.35+d*0.0015)
    
    canvas.draw()
