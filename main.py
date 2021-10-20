import numpy as np

# Global Variables
genSize = 1000
muteRate = 0.0001
numberOfGens = 100
maxUtility = None

# utilities, weights, and knapsacks are linked via index
utilities = list() # list of all utilities
weights = list()    # list of all weights


##### CLASS AND METHODS #####
class Solution:

    def __init__(self, *inp):

        #declaring instance variables
        self.knapsack = np.zeros(400, dtype=bool)
        self.totalUtil = float()
        self.weight = float()
        self.normal = float()
        self.cumNorm = float()

        if len(inp) == 0:
            self.constructZero()

        elif len(inp) == 1:
            self.constructOne(inp)

    # builds a solution with no starting information
    def constructZero(self):
        global weights
        self.totalUtil = 0
        self.weight = 0
        count = 0
        while self.weight < 500 or count < 20: # or self.weight < 500
            temp = np.random.randint(0, 400) # generate a random index
            # if (self.weight + weights[temp]) > 500: break # keeps any solution in initial generation from being over 500lbs
            self.knapsack[temp] = 1 # declare random index as a piece of gear to be taken
            self.weight += weights[temp]
            self.totalUtil += utilities[temp]
            count += 1
        self.totalUtil = round(self.totalUtil, 2)
        self.weight = round(self.weight, 2)

    # builds a solution based on given knapsack
    def constructOne(self, inp):
        self.knapsack = inp[0]
        self.totalUtil = 0
        self.weight = 0
        for i in self.knapsack:
            if i == 1:
                self.totalUtil += utilities[i]
                self.weight += weights[i]
        self.totalUtil = round(self.totalUtil, 2)
        self.weight = round(self.weight, 2)
        if self.weight > 500:
            self.totalUtil = 1
            # self.avgUtil = 1
        # else: print("totalUtil = {}  weight = {}".format(self.totalUtil, self.weight))

    # applys mutation to a solutions knapsack
    def mutation(self):
        for i in range(len(self.knapsack)):
            if np.random.rand() < muteRate:
                # print("index: {} value: {}".format(i, self.knapsack[i]))
                self.knapsack[i] = ~self.knapsack[i]


    # def getSolutionAve(self):
    #     self.avgUtil = 0
    #     for i in range(len(self.knapsack)):
    #         self.avgUtil += weights[i]
    #     self.avgUtil /= len(self.knapsack)
    #     return self.avgUtil

##### FUNCTIONS #####
# function for sorting a generation based on TOTAL utility score
def selectSort(generation: list):
    for i in range(len(generation)):
        index = i
        for j in range(i + 1, len(generation)):
            if generation[index].totalUtil > generation[j].totalUtil:
                index = j

        generation[i], generation[index] = generation[index], generation[i]


# prints out all avgUtil values for a generation
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
        squaredSum += np.square(i.totalUtil)

    for i in generation:
        temp = np.square(i.totalUtil) / squaredSum
        i.normal = round(temp, 5)


# finds the cumulative normal value for all elements in a generation
def getCumNorm(generation: list):
    for i in generation:
        for j in generation:
            if i == j: break
            else: i.cumNorm += j.normal
        i.cumNorm = round(i.cumNorm, 5)


# finds the average utility score of a generation and finds max Solution Fitness in a generation
def getUtilities(generation: list):
    global maxUtility
    average = 0
    for i in generation:
        average += i.totalUtil
        if i.totalUtil > maxUtility.totalUtil: maxUtility = i
    return round(average/len(generation), 3)


# finds the average weight of all solutions in a generation
def getAveWeight(generation: list):
    average = 0
    for i in generation:
        average += i.weight
    return round(average/len(generation), 3)


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
        child.mutation()
        if child.weight < 500: generation.append(child)

        # creating child two
        temp1, temp2 = generation[mama].knapsack[split:], generation[papa].knapsack[:split]
        child = Solution(np.concatenate([temp1, temp2]))
        child.mutation()
        if child.weight < 500: generation.append(child)


if __name__ == "__main__":
    # reading in all values, convert to float, and store in specified list
    with open('Program2Input.txt', 'r') as file:
        for i in file:
            temp = i.split() # (utility, weight)
            utilities.append(float(temp[0]))
            weights.append(float(temp[1]))

    maxUtility = Solution()

    # creating a initial population of 1000 random solutions
    currentGen = list()
    for i in range(genSize):
        currentGen.append(Solution())


    for i in range(numberOfGens):
        selectSort(currentGen)
        normalize(currentGen)
        getCumNorm(currentGen)
        newGen = selection(currentGen)
        crossover(newGen)
        aveUtility = getUtilities(newGen)
        # print("gen {}: maxUtility = {}\t\taveUtility = {}\t\tweight = {}".format(i, maxUtility.totalUtil, aveUtility, getAveWeight(newGen)))
        print("gen {}: maxUtility = {} :\t".format(i, maxUtility.totalUtil), end="")
        printGenUtil(newGen)
        currentGen = newGen
        newGen = None

    # ##### TEST CODE #####
    # print("Gen Weights = ", end="")
    # for i in currentGen:
    #     print(i.weight, end=", ")
    # print('\n')
    #
    # print("Pre-Selection: ", end="")
    # printGenUtil(currentGen)
    # print()
    #
    # normalize(currentGen)
    # getCumNorm(currentGen)
    # newGen = selection(currentGen)
    # print("Post-Selection: ", end="")
    # printGenUtil(newGen)
    # print()
    #
    # crossover(newGen)
    # print("Post-Crossover: ", end="")
    # printGenUtil(newGen)
    #
    # temp1 = newGen[1].knapsack
    # newGen[1].mutation()
    # temp2 = newGen[1].knapsack
    # print(np.array_equal(temp1, temp2))
