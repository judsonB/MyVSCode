def dizzySquatch(directions):
  x = 0
  y = 0
  text = ""
  for dir in directions:
    if dir == "North":
      y += 1
    elif dir == "East":
      x += 1
    elif dir == "South":
      y -= 1
    else:
      x -= 1
    text += f"({x}, {y}) - "
    if x <= 4 and x >= -4 and y <= 4 and y >= -4:
      text += "safe"
    elif x <= 7 and x >= -7 and y <= 7 and y >= -7:
      text += "close..."
    elif x <= 8 and x >= -8 and y <= 8 and y >= -8:
      text += "Tipping!!!!!"
    else:
      text += "Splash!\n"
      text += "Sasquatch Fell!"
      return(text)
    text += "\n"
  text += "Sasquatch stayed on the platform!"
  return text

# f = open("02_cardinals.txt", "r")
# numLines = int(f.readline())
# for i in range(numLines):
#   line = f.readline()
#   list = line.split(", ")
#   print(dizzySquatch(list))

numLines = int(input())
for i in range(numLines):
  line = input()
  list = line.split(", ")
  print(dizzySquatch(list))