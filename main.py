import numpy
import random

class Solution:

    # constructor for creating a random solution
    def __init__(self, gear):

        self.knapsack = list()
        self.totalUtil = 0
        self.totalWeig = 0

        while self.totalWeig < 500 or len(self.knapsack) < 20:
            temp = gear[numpy.random.randint(0, 400)]
            self.knapsack.append(temp)
            self.totalWeig += temp[1]
            self.totalUtil += temp[0]
 #       print("solution = ", self.knapsack, "\nlength = ", len(self.knapsack), "\ntotal weight = ", self.totalWeig, "\ntotal utility = ", self.totalUtil, "\n")

    # constructor for creating a solution based on two parents
    # def __int__(self, parents):
    #     population = []
    #

    def mutation(self, muteRate):
        # if a randomly generated value is less than the given mutation rate (0.0001) then a mutation *should* occur
        # each element in the list has an independent chance of mutation
        for i in range(len(self.knapsack)):
            if numpy.random.random() < muteRate:
                print("true")
                self.knapsack[i][1] = round(random.uniform(0.0, 25.0), 1)


# number of combinations (spec = 1000)
popSize = 10
# likelihood of a mutation happening (spec = 0.0001
muteRate = 0.1

# list of all possible items (utility, weight)
gear = []

# read in all values and convert to float
with open('Program2Input.txt', 'r') as file:
    count = 0
    for i in file:
        gear.append(i.split())
        gear[count][0] = float(gear[count][0])
        gear[count][1] = float(gear[count][1])
        count += 1


# creating a number(popSize) of combinations and putting them in generation list
generation = list()
for i in range(popSize):
    generation.append(Solution(gear))
# cannot get key to reference utility value in class
# generation.sort(key=generation[1].getUtility())
# sort(generation.totalUtil)

for i in range(popSize):
    index = i
    for j in range(i+1, popSize):
        if generation[index].totalUtil > generation[j].totalUtil:
            index = j

    generation[i], generation[index] = generation[index], generation[i]

print(generation[0].knapsack)
generation[0].mutation(muteRate)
print(generation[0].knapsack)

