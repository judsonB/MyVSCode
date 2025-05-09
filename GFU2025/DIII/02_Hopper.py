numSets = int(input())
goodLeadsCount = 0
for i in range(numSets):
  txt = input().lower()
  newTxt = ""
  for j in range(len(txt)):
    if (txt[j] == " " or txt[j] >= "a" and txt[j] <= "z"):
      newTxt += txt[j]
  words = newTxt.split(" ")
  primary = words[0]
  words.remove(primary)
  if primary in words:
    print("Good Lead")
    goodLeadsCount += 1
  else:
    print("Bad Lead")
print(goodLeadsCount)