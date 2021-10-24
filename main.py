import numpy as np

genSize = 500
muteRate = 0.0001
numberOfGens = 5000
itemsPerSolution = 20

weights = list()
utilities = list()


##### CLASS #####
# holds all information for each individual solution to the knapsack problem
class Solution:

    # init method holds instance variables and calls to two constructors based on given arguments
    def __init__(self, *inp):
        self.knapsack = np.zeros(400, dtype=bool)
        self.weight = float()
        self.utility = float()
        self.normal = float()

        if len(inp) == 0:
            self.constructZero()

        elif len(inp) == 1:
            self.constructOne(inp)

    # constructor builds a random solution (mostly used for builidng initial generation)
    def constructZero(self):
        self.weight = self.utility = 0
        for i in range(itemsPerSolution):
            item = np.random.randint(400)
            self.knapsack[item] = 1
            self.weight += weights[item]
            self.utility += utilities[item]
        self.weight = round(self.weight, 2)
        self.utility = round(self.utility, 2)

    # constructor builds a solution based on given knapsack
    def constructOne(self, inp):
        self.weight = self.utility = 0
        self.knapsack = inp[0]
        for i in range(len(self.knapsack)):
            if self.knapsack[i]:
                self.weight += weights[i]
                self.utility += utilities[i]
        self.weight = round(self.weight, 2)
        self.utility = round(self.utility, 2)

        if self.weight > 500:
            self.utility = 1

    # applies a 1/1000 chance of any bit in the knapsack being flipped
    def mutation(self):
        for i in range(len(self.knapsack)):
            check = np.random.rand()
            if check < muteRate:
                self.knapsack[i] = ~self.knapsack[i]


##### FUNCTIONS #####
def normalize(generation: list):
    squaredSum = 0
    for i in generation:
        squaredSum += np.square(i.utility)

    for i in generation:
        i.normal = np.square(i.utility) / squaredSum


# basic roulette selection
def selection(generation: list):
    sum = 0
    check = np.random.rand()

    for i in range(len(generation)):
        sum += generation[i].normal
        if sum < check < (sum + generation[i+1].normal):
            return i+1


# applies crossover to two parents, creates two children
def crossover(mama: Solution, papa: Solution):
    split = np.random.randint(0, 400)
    child1 = Solution(np.concatenate([mama.knapsack[:split], papa.knapsack[split:]]))
    child2 = Solution(np.concatenate([papa.knapsack[:split], mama.knapsack[split:]]))

    return child1, child2


# print out all utilities in given generation
def printGenUtil(generation: list):
    for i in generation:
        print(i.utility, end=', ')
    print()


# print out all weights in given generation
def printGenWeight(generation: list):
    for i in generation:
        print(i.weight, end=', ')
    print()


# returns the average utility of a generation
def getGenUtilAve(generation: list):
    sum = 0
    for i in generation:
        sum += i.utility

    return round(sum / len(generation), 3)


##### MAIN #####
if __name__ == "__main__":
    # read in all values from file, store in specified list
    with open("Program2Input.txt", 'r') as file:
        for i in file:
            temp = i.split()
            utilities.append(float(temp[0]))
            weights.append(float(temp[1]))

    currentGen = list()
    for i in range(genSize):
        z = Solution()
        z.mutation()
        currentGen.append(z)

    maxUtility = Solution()
    for i in range(numberOfGens):

        currentGen.sort(key=lambda u: u.utility)
        newGen = list()
        normalize(currentGen)

        while len(newGen) < genSize:
            mamaInd = selection(currentGen)
            papaInd = selection(currentGen)
            # restarts loop if mama index or papa index is not assigned to a value
            if type(mamaInd) != int or type(papaInd) != int: continue

            mama, papa = currentGen[mamaInd], currentGen[papaInd]
            child1, child2 = crossover(mama, papa)
            mama.mutation(), papa.mutation(), child2.mutation(), child1.mutation()

            if mama.utility > maxUtility.utility: maxUtility = mama
            if papa.utility > maxUtility.utility: maxUtility = papa
            if child1.utility > maxUtility.utility: maxUtility = child1
            if child2.utility > maxUtility.utility: maxUtility = child2

            newGen.append(mama), newGen.append(papa)
            newGen.append(child2), newGen.append(child1)

        currentGen.sort(key= lambda u: u.utility)
        print("Gen {}: maxUtil = {} aveUtil = {}".format(i, maxUtility.utility, getGenUtilAve(currentGen)), end=""), printGenUtil(currentGen)
        # print("Gen {}: average utility: ".format(i), end=""), printGenUtilAve(newGen)
        currentGen = newGen

