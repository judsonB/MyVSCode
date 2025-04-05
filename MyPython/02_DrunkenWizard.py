from random import randint
x = 0
y = 0
maxX = 0
maxY = 0
minX = 0
minY = 0
for i in range(100):
  dir = randint(1, 4)
  if(dir == 1):
    y += 1
  elif dir == 2:
    x += 1
  elif dir == 3:
    y -= 1
  else:
    x -= 1
  maxX = max(x, maxX)
  maxY = max(y, maxY)
  minX = min(x, minX)
  minY = min(y, minY)
print(f"({x}, {y})")
print(f"MinX: {minX}")
print(f"MinY: {minY}")
print(f"MaxX: {maxX}")
print(f"MaxY: {maxY}")