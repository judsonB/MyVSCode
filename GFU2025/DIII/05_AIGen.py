"""
  5. Caffeine Anhydrous
  The greatest of discoveries, Caffeine!
  As you gather your tribe and arrive in the promised land you discover that the food promised to you was no ordinary food, but a large supply of sugar, salt, and caffeine! Though in amounts large enough both salt and caffeine will kill you, the combination of small parts of the two in conjunction with large amounts of sugar has given you enough energy to kick-start the growth of a new civilization.
  
  Input
  The first input will contain a single integer n that indicates the number of data sets that follow. Each data set will contain three integers, which correspond in order to the sugar, salt, and caffeine content of a portion of the food.
  
  Output
  For each data set, output a matrix composed of the word isopod as its border and the character & as its interior with a side length equal to the minimum of the three integer values. Each outputted matrix will be followed by a blank line.

  Example Input
  3
  1 2 3
  3 4 5
  6 7 9

  Example Output to Screen
  i

  iso
  s&p
  ido

  isopod
  s&&&&i
  i&&&&s
  d&&&&o
  o&&&&p
  posido
"""
val = int(input())

for _ in range(val):
  sugar, salt, caffeine = map(int, input().split())
  side_length = min(sugar, salt, caffeine)
  
  if side_length == 0:
    print()
    continue  
  
  border = "isopod"
  for i in range(side_length):
    if i == 0 or i == side_length - 1:
      print(border[:side_length])
    else:
      print(border[i] + "&" * (side_length - 2) + border[side_length - i - 1])
  print()
