from math import *
SEEDS_PER_POUND = 4000
# Fee = 100 seeds per pound, per inch 
numSets = int(input())
for i in range(numSets):
  seedsInPile, distance = input().split()
  seedsInPile = int(seedsInPile)
  distance = int(distance)
  fee = seedsInPile / SEEDS_PER_POUND * 100 * distance
  print(f"{ceil(fee)} seeds paid in compensation for {fee:.2f} lbs/inch total")