import numpy as np


##### CLASS AND METHODS #####
class Solution:

    def __init__(self, *inp):

        #declaring instance variables
        self.knapsack = np.zeros(400, dtype=int)
        self.totalUtil = float()
        self.avgUtil = float()
        self.weight = float()
        self.normal = float()
        self.cumNorm = float()

        if len(inp) == 0:
            self.constructZero()

        elif len(inp) == 1:
            self.constructOne(inp)

    def constructZero(self):
        self.totalUtil = 0
        self.weight = 0
        count = 0
        while self.weight <= 500 or count < 20:
            temp = np.random.randint(0, 400) # generate a random index
            if (self.weight + weights[temp]) > 500: break
            self.knapsack[temp] = 1 # declare random index as a piece of gear to be taken
            self.weight += weights[temp]
            self.totalUtil += utilities[temp]
            self.avgUtil += weights[temp]
            count += 1
        self.totalUtil = round(self.totalUtil, 2)
        self.weight = round(self.weight, 2)
        self.avgUtil = round(self.avgUtil/len(self.knapsack), 2)

    def constructOne(self, inp):
        self.knapsack = inp[0]
        self.totalUtil = 0
        self.weight = 0
        for i in self.knapsack:
            if i == 1:
                self.totalUtil += utilities[i]
                self.weight += weights[i]
                self.avgUtil += utilities[i]
        self.totalUtil = round(self.totalUtil, 2)
        self.weight = round(self.weight, 2)
        if self.weight > 500:
            self.totalUtil = 1
            self.avgUtil = 1
        self.avgUtil = round(self.avgUtil / len(self.knapsack), 2)
        print("totalUtil = {}  weight = {}".format(self.totalUtil, self.weight))

    def getAverage(self):
        self.avgUtil = 0
        for i in range(len(self.knapsack)):
            self.avgUtil += weights[i]
        self.avgUtil /= len(self.knapsack)
        return self.avgUtil

##### FUNCTIONS #####


# function for sorting a generation based on TOTAL utility score
def selectSort(generation: list):
    for i in range(len(generation)):
        index = i
        for j in range(i + 1, len(generation)):
            if generation[index].totalUtil > generation[j].totalUtil:
                index = j

        generation[i], generation[index] = generation[index], generation[i]


# prints out all totalUtil values for a generation
def printGenUtil(generation: list):
    selectSort(generation)
    for i in range(len(generation)):
        print(generation[i].totalUtil, end=", ")
    print()


# prints out all normal values for a generation
def printNormal(generation: list):
    selectSort(generation)
    for i in generation:
        print(i.normal, end=", ")
    print()


# applying L2 normalization to the average utilities of a generation
def normalize(generation: list):
    squaredSum = 0
    for i in generation:
        squaredSum += np.square(i.avgUtil)

    for i in generation:
        temp = np.square(i.avgUtil) / squaredSum
        i.normal = round(temp, 5)


# finds the cumulative normal value for all elements in a generation
def getCumNorm(generation: list):
    for i in generation:
        for j in generation:
            if i == j: break
            else: i.cumNorm += j.normal
        i.cumNorm = round(i.cumNorm, 5)


# applies roulette wheel selection by comparing the cumulative normal value to a random value
def selection(generation: list):
    newGen = list()
    for i in generation:
        checkVal = np.random.rand()
        if checkVal < i.cumNorm:
            newGen.append(i)

    return newGen


# applying crossover to solutions that remain after selection to repopulate generation
def crossover(generation: list):
    while len(generation) < genSize:
        # generate a random mother, father, and split value
        papa, mama = np.random.randint(0, len(generation)), np.random.randint(0, len(generation))
        split = np.random.randint(0, 400)
        # creating child one
        temp1, temp2 = generation[mama].knapsack[:split], generation[papa].knapsack[split:]
        child = Solution(np.concatenate([temp1, temp2]))
        if child.weight < 500:
            generation.append(child)

        # creating child two
        temp1, temp2 = generation[mama].knapsack[split:], generation[papa].knapsack[:split]
        child = Solution(np.concatenate([temp1, temp2]))
        if child.weight < 500:
            generation.append(child)


# Global Variables
genSize = 1000
muteRate = 0.0001
numberOfGens = 100

# utilities, weights, and knapsacks are linked via index
utilities = list() # list of all utilities
weights = list()    # list of all weights


# reading in all values, convert to float, and store in specified list
with open('Program2Input.txt', 'r') as file:
    for i in file:
        temp = i.split() # (utility, weight)
        utilities.append(float(temp[0]))
        weights.append(float(temp[1]))

# creating a initial population of 1000 random solutions
currentGen = list()
for i in range(genSize):
    currentGen.append(Solution())

print("Gen Weights = ", end="")
for i in currentGen:
    print(i.weight, end=", ")
print()

print("Pre-Selection: ", end="")
printGenUtil(currentGen)
print()

normalize(currentGen)
getCumNorm(currentGen)
newGen = selection(currentGen)
print("Post-Selection: ", end="")
printGenUtil(newGen)
print()

crossover(newGen)
print("Post-Crossover: ", end="")
printGenUtil(newGen)



