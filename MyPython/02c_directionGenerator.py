from random import randint
for i in range(10):
  text = ""
  numVals = randint(20,100)
  for j in range(numVals):
    dir = randint(1, 4)
    if(dir == 1):
      text += "North"
    elif dir == 2:
      text += "East"
    elif dir == 3:
      text += "South"
    else:
      text += "West"
    if (j < numVals-1):
      text += ", "
  print(text)
  print()
