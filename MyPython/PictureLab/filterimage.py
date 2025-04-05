from ezgraphics import GraphicsImage, GraphicsWindow
folder = "PictureLab/"
filename = "IMG_1230.gif"
image = GraphicsImage(folder+filename)

width = image.width()
height = image.height()
redSum = 0;
greenSum = 0;
blueSum = 0;
for row in range(height):
  for col in range(width):
    red = image.getRed(row, col)
    green = image.getGreen(row, col)
    blue = image.getBlue(row, col)
    redSum += red
    greenSum += green
    blueSum += blue
    red *= 1
    red = min(red, 255)
    red = int(red)
    #green *= 2
    #green = min(green, 255)
    # blue *= 2
    # blue = min(blue, 255)
    image.setPixel(row, col, red, green, blue)
print(redSum/(width * height))
print(greenSum/(width * height))
print(blueSum/(width * height))
win = GraphicsWindow()
canvas = win.canvas()
canvas.drawImage(image)
win.wait()

#image.save(folder + "negative-"+filename)