import imagewells

images = imagewells.loadImageWell(minsize=(800,600))
img = choice(images['allimages'])
print(img)

image( img, 0,0, width=800 )
