import random

f = open("Program2Input.txt", 'r')
# list of all possible items
gear = []

for i in f:
    temp = i.split()
    gear.append(temp)

print(gear)
popSize = 1000
muteRate = 0.0001

population = []
for i in range(popSize):
    population.append(gear[random.randint(0,401)])