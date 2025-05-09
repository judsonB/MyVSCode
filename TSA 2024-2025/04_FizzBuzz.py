stop = int(input("Enter a number: "))
txt = ""
for i in range(1, stop + 1):
  if i % 3 == 0 and i % 5 == 0:
    txt += " Fizzbuzz"
  elif i % 3 == 0:
    txt += " Fizz"
  elif i % 5 == 0:
    txt += " Buzz"
  else:
    txt += " "+str(i)
txt = txt.strip()
print(txt)
