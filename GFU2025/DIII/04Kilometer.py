#from math import *
def getGrid():
  grid = []
  for i in range(5):
    grid.append(list(input()))
  input()#clear blank line
  return grid
def printGrid(grid):
  for row in grid:
    txt = ""
    for symbol in row:
      txt += symbol + ""
    print(txt)
def isValidLoc(row, col):
  if row >= 0 and col >= 0 and row < 5 and col <5:
    return True
  return False
def isConnected(grid, row, col):
  if(grid[row][col] == "&"):
    return True
  return False
def traversePath(grid, row, col):
  list = []
  list.append([row, col])
  count = 0
  while(len(list) > 0):
    row, col = list.pop()
    if(grid[row][col] == "&"):
      count += 1
      grid[row][col] = "X"
      if(isValidLoc(row-1, col) and isConnected(grid, row-1, col)):
        list.append([row-1, col])
      if(isValidLoc(row+1, col) and isConnected(grid, row+1, col)):
        list.append([row+1, col])
      if(isValidLoc(row, col-1) and isConnected(grid, row, col-1)):
        list.append([row, col-1])
      if(isValidLoc(row, col+1) and isConnected(grid, row, col+1)):
        list.append([row, col+1])
  return count
def findBiggestCluster(grid):
  biggest = 0
  for row in range(len(grid)):
    for col in range(len(grid[row])):
      if grid[row][col] == "&":
        count = traversePath(grid, row, col)
        if count > biggest:
          biggest = count      
  print(biggest)


numSets = int(input())
for i in range(numSets):
  grid = getGrid()
  findBiggestCluster(grid)
  #printGrid(grid)