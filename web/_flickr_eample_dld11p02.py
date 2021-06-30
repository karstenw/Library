import web
images = web.flickr.search("wolf", count=50)
n = len(images)
print(images)

size(800,800)

for i in images:
    img = i.download()
    rotate(-45+random(90))
    image(img, x=50+random(WIDTH-100), y=50+random(HEIGHT-100), width=150, height=150, alpha=60)

