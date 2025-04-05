from PIL import Image, ImageDraw


noteRange = None
melodyMap = []
durationMap = []
with open('MelodyMap/HoldingHandsVerseA.txt', 'r') as file:
    # Read the contents of the file
    for line in file:
        if(noteRange == None):
            noteRange = line.split()
        elif melodyMap == None or len(melodyMap) == len(durationMap):
            melodyMap.append(line.split())
        else:
            durationMap.append(line.split())
print(noteRange)
print("---------")
print(melodyMap)
    
# Create a blank image
radius = 20
img_width = 2800
img_height = radius+2*radius*len(noteRange)
image = Image.new('RGB', (img_width, img_height), 'white')
draw = ImageDraw.Draw(image)

# Define the circle parameters
x = 0
y = 0
color = 'red'
for note in noteRange:
    y+=radius*2
    draw.line([(0, y), (img_width, y)], fill=color, width=1)
for x in range(radius*4, img_width, radius * 16):
    draw.line([(x, 0), (x, img_height)], fill=color, width=1)


x = 0
y = 0
for i in range(len(melodyMap)):
    melodySet = melodyMap[i]
    durationSet = durationMap[i]
    for j in range(len(melodySet)):
        note = melodySet[j]
        duration = float(durationSet[j])
        color = 'hotpink'
        out = 'white'
        if duration%1 == .5:
            out='black'
        if duration == .5:
            color= 'red'
        if duration == 1:
            color= 'orange'
        elif duration == 1.5:
            color= 'yellow'
        elif duration == 2:
            color= 'green'
        elif duration == 3:
            color= 'blue'
        elif duration == 4:
            color= 'indigo'
        elif duration == 6:
            color = "fuchsia"

        duration *= radius
        x += duration
        y = noteRange.index(note)*(2*radius)+radius
        
        
        # Draw the circle
        draw.ellipse((x - duration, y - radius, x + duration, y + radius), fill=color, outline=out, width=4)
        x += duration

# Save or display the image
image.show()