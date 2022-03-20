try:
    supershape = ximport("supershape")
except:
    supershape = ximport("__init__")
    # reload(supershape)

size(600, 400)

nofill()
stroke(0)

font("Times", 200)
path = textpath("FUN!", 50, 250)

for contour in path.contours:
    contour = supershape.transform(contour, 50, 0.25, 3.5, 3.5)
    drawpath(contour)
