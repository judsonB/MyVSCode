text = input()
text = text.lower();
weight = 0
for symbol in text:
  if symbol == " " or symbol == "a" or symbol == "e" or symbol == "i" or symbol == "o" or symbol == "u":
    weight += 1
  else:
    weight -= 1
print(weight)
if weight == 0:
  print("The text is balanced.")
elif weight > 0:
  print("Too many vowels & spaces.")
else:
  print("Too many consonants.")