import numpy
import random


# function for sorting a generation based on utility score
def selectSort(generation: list):
    for i in range(popSize):
        index = i
        for j in range(i + 1, popSize):
            if generation[index].utility > generation[j].utility:
                index = j

        generation[i], generation[index] = generation[index], generation[i]

    # function decides which solutions of the previous generation will create the next generation
    # currently it takes the better half of generation, based on utility
def selection(generation: list):
    selectSort(generation)
    index = len(generation)//2
    if index % 2 == 1:
        index += 1
    generation = generation[index:]
    return generation

    # prints out a list of all utilities in a generation
def printGenUtil(generation: list):
    for i in range(len(generation)):
        print(generation[i].utility, end=", ")
    print()

# function performs L2 normalization (squared) on utility values of a generation
def normalize(generation: list):
    squaredSum = 0 # the sum of squared utility
    for i in range(len(generation)):
        squaredSum += numpy.square(generation[i].utility)

    for i in range(len(generation)):
        generation[i].normal = numpy.square(generation[i].utility) / squaredSum


def getAverage(generation: list):
    average = 0
    for i in range(len(generation)):
        average += generation[i].utility
    average /= len(generation)
    return average

class Solution:

    # attempting to implement constructors for specific arguments
    # constructor for creating a random solution
    def __init__(self, *inp):
        # declaring instance variables
        self.knapsack = list()
        self.utility = 0
        self.weight = 0
        self.normal = 0

        # execute constructor function if one argument is given
        if len(inp) == 1:
            self.constructor(inp)

        # execute crossover function if two arguments are given
        elif len(inp) == 2:
            self.crossover(inp)

    # default construction, when a random solution is needed
    # argument is list of gear
    def constructor(self, args):
        while self.weight < 200 or len(self.knapsack) < 20:
            temp = gear[numpy.random.randint(0, 400)]
            self.knapsack.append(temp)
            self.weight += temp[1]
            self.utility += temp[0]

        # rounding for readability
        self.utility, self.weight = round(self.utility, 2), round(self.weight, 2)
        # print("solution = ", self.knapsack, "\nlength = ", len(self.knapsack), "\ntotal weight = ", self.totalWeig, "\ntotal utility = ", self.totalUtil, "\n")

    # method creates a new solution by randomly splicing two parents together
    # constructor for creating a new solution by randomly splicing two parents, this is where CROSSOVER takes place
    # argument is two knapsack lists, not whole solutions, one mama and one papa
    def crossover(self, args):
        split = random.randint(0, len(args[0]))
        self.knapsack = args[0][:split] + args[1][split:]
        # test
        print("mama = ", args[0], "\npapa = ", args[1], "\nsplit = ", split, "\nchild = ", self.knapsack)
        self.mutation(muteRate)

    def mutation(self, muteRate):
        # if a randomly generated value is less than the given mutation rate (0.0001) then a mutation *should* occur
        # each element in the list has an independent chance of mutation
        for i in range(len(self.knapsack)):
            if numpy.random.random() < muteRate:
                # print("true at {}".format(i), "\tvalue before =", self.knapsack[i])
                self.knapsack[i][1] = round(random.uniform(0.0, 25.0), 3)
                # print("value after =", self.knapsack[i])
                # print("child = ", self.knapsack)

    def getTotalWeight(self):
        for i in range(len(self.knapsack)):
            self.weight += self.knapsack[1]
        return self.weight

    def getTotalUtility(self):
        for i in range(len(self.knapsack)):
            self.utility += self.knapsack[0]
        return self.utility


##### MAIN #####
# number of combinations (spec = 1000)
popSize = 1000
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



##### Testing #####

printGenUtil(generation)
generation = selection(generation)
printGenUtil(generation)

#print(getAverage(generation))



#
# generation = selection(generation)
# needed = popSize - len(generation)
# for i in range(needed):
#     mama = random.randint(0, len(generation))
#     papa = random.randint(0, len(generation))
#     generation.append(Solution(generation[mama], generation[papa]))
#





