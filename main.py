import numpy
import random

def selectSort(generation: list):
    for i in range(popSize):
        index = i
        for j in range(i + 1, popSize):
            if generation[index].totalUtil > generation[j].totalUtil:
                index = j

        generation[i], generation[index] = generation[index], generation[i]


def selection(generation: list):
    selectSort(generation)
    index = len(generation)//2
    if index % 2 == 1:
        index += 1
    generation = generation[index:]
    return generation


class Solution:

    # attempting to implement constructors for specific arguments
    # constructor for creating a random solution
    def __init__(self, *num):
        # default construction, when a random solution is needed
        # argument is list of gear
        if len(num) == 2:
            self.knapsack = list()
            self.totalUtil = 0
            self.totalWeig = 0

            while self.totalWeig < 500 or len(self.knapsack) < 20:
                temp = gear[numpy.random.randint(0, 400)]
                self.knapsack.append(temp)
                self.totalWeig += temp[1]
                self.totalUtil += temp[0]

            # rounding for readability
            self.totalUtil, self.totalWeig = round(self.totalUtil, 2), round(self.totalWeig, 2)
            # print("solution = ", self.knapsack, "\nlength = ", len(self.knapsack), "\ntotal weight = ", self.totalWeig, "\ntotal utility = ", self.totalUtil, "\n")

        # constructor for creating a solution based on two parents, this is where CROSSOVER takes place
        # argument is two solutions, one mama and one papa
        elif len(num) == 3:
            split = random.randint(0, len(num[0]))
            self.knapsack = num[0][:split] + num[1][split:]

    def mutation(self, muteRate):
        # if a randomly generated value is less than the given mutation rate (0.0001) then a mutation *should* occur
        # each element in the list has an independent chance of mutation
        for i in range(len(self.knapsack)):
            if numpy.random.random() < muteRate:
                self.knapsack[i][1] = round(random.uniform(0.0, 25.0), 1)


# number of combinations (spec = 1000)
popSize = 10
# likelihood of a mutation happening (spec = 0.0001)
muteRate = 0.0001

# list of all possible items (utility, weight)
gear = []

# read in all values and convert to float
with open('Program2Input.txt', 'r') as file:
    count = 0
    for i in file:
        gear.append(i.split())
        gear[count][0], gear[count][1] = float(gear[count][0]), float(gear[count][1])
        count += 1


# creating a number(popSize) of combinations and putting them in generation list
generation = list()
for i in range(popSize):
    generation.append(Solution(gear))
# cannot get key to reference utility value in class
# generation.sort(key=generation[1].getUtility())
# sort(generation.totalUtil)

generation = selection(generation)
needed = popSize - len(generation)
for i in range(needed):
    mama = random.randint(0, len(generation))
    papa = random.randint(0, len(generation))
    generation.append(Solution(generation[mama], generation[papa]))




## Testing
for i in range(popSize):
    print(generation[i].totalUtil, end=", ")
print("length = ", len(generation))

#selectSort(generation)
generation = selection(generation)

for i in range(len(generation)):
    print(generation[i].totalUtil, end=", ")
print("length = ", len(generation))


