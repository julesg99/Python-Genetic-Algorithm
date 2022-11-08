# imports
import numpy as np
from matplotlib import pyplot as plt

# global variables
genSize = 1000
muteRate = 0.0001
numberOfGens = 5000
itemsPerSolution = 20

# lists for storing input values
weights = list()
utilities = list()

##### CLASS #####

# holds all information for each individual solution to the knapsack problem
class Solution:

    # init method holds instance variables and calls to two constructors based on given arguments
    def __init__(self, *inp) -> None:
        self.knapsack = np.zeros(400, dtype=bool)
        self.weight, self.utility, self.normal = float(), float(), float()

        if len(inp) == 0:
            self.constructZero()

        elif len(inp) == 1:
            self.constructOne(inp)

    # constructor builds a random solution (mostly used for building initial generation)
    def constructZero(self) -> None:
        self.weight = self.utility = 0
        for i in range(itemsPerSolution):
            item = np.random.randint(400)
            self.knapsack[item] = 1
            self.weight += weights[item]
            self.utility += utilities[item]
        self.weight = round(self.weight, 2)
        self.utility = round(self.utility, 2)

    # constructor builds a solution based on given knapsack
    def constructOne(self, inp) -> None:
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
    def mutation(self) -> None:
        for i in range(len(self.knapsack)):
            check = np.random.rand()
            if check < muteRate:
                self.knapsack[i] = ~self.knapsack[i]


##### FUNCTIONS #####

# apply L2 normalization to generation so values are on the same scale
def normalize(generation: list) -> None:
    squaredSum = 0
    # square all values and sum
    for i in generation:
        squaredSum += np.square(i.utility)

    # divide squared utility value by squared sum
    for i in generation:
        i.normal = np.square(i.utility) / squaredSum


# basic roulette selection
def selection(generation: list) -> int:
    sum = 0
    check = np.random.rand()

    # sum all normalized utility values until check value is between the sum of current and sum of next
    for i in range(len(generation)):
        sum += generation[i].normal
        if sum < check < (sum + generation[i+1].normal):
            return i+1


# applies crossover to two parents, creates two children
def crossover(mama: Solution, papa: Solution) -> [Solution, Solution]:
    # randomly decide where to split parents
    split = np.random.randint(0, 400)
    child1 = Solution(np.concatenate([mama.knapsack[:split], papa.knapsack[split:]]))
    child2 = Solution(np.concatenate([papa.knapsack[:split], mama.knapsack[split:]]))

    return child1, child2


# print out all utilities in given generation
def printGenUtil(generation: list) -> None:
    for i in generation:
        print(i.utility, end=', ')
    print()


# print out all weights in given generation
def printGenWeight(generation: list) -> None:
    for i in generation:
        print(i.weight, end=', ')
    print()


# returns the average utility of a generation
def getGenUtilAve(generation: list) -> float:
    sum = 0
    for i in generation:
        sum += i.utility

    return round(sum / len(generation), 3)


##### MAIN #####
if __name__ == "__main__":

    # read in all values from file, store in specified list
    with open("input.txt", 'r') as file:
        for i in file:
            temp = i.split()
            utilities.append(float(temp[0]))
            weights.append(float(temp[1]))

    # after read operation is complete, open output file
    file = open("output.txt", 'w')

    # create variable to store current working generations
    currentGen = list()
    # create generation size solutions and apply a random mutation
    for i in range(genSize):
        z = Solution()
        z.mutation()
        currentGen.append(z)

    # currently unused
    # intended to help track change in generational average utility
    aveUtility = list()

    # tracks max utility of any single solution found
    maxUtility = Solution()

    # primary loop
    for i in range(numberOfGens):

        # sort current generation by ascending utility value of each solution
        currentGen.sort(key=lambda u: u.utility)

        # normalize working generation
        normalize(currentGen)

        # new list for building next generation
        newGen = list()

        # loop builds generation through selection, crossover, and mutation
        # loop also checks and updates max utility value
        while len(newGen) < genSize:

            # call method to randomly select index for mama and papa
            mamaInd, papaInd = selection(currentGen), selection(currentGen)

            # restarts loop if mama index or papa index is not assigned to a value
            if type(mamaInd) != int or type(papaInd) != int: continue

            # use index to get mama and papa solution
            mama, papa = currentGen[mamaInd], currentGen[papaInd]

            # apply crossover to parents and get children
            child1, child2 = crossover(mama, papa)

            # apply mutation to parents and children
            mama.mutation(), papa.mutation(), child2.mutation(), child1.mutation()

            # check if any solution has a greater utility than current max
            if mama.utility > maxUtility.utility: maxUtility = mama
            elif papa.utility > maxUtility.utility: maxUtility = papa
            elif child1.utility > maxUtility.utility: maxUtility = child1
            elif child2.utility > maxUtility.utility: maxUtility = child2

            # add parents and children to generation
            newGen.extend([mama, papa, child2, child1])

        # checking to see if average utility changes more than 0.01 in ten generations
        aveUtility.append(getGenUtilAve(newGen))
        if getGenUtilAve(newGen) > 600:
            index = len(aveUtility)-1
            check = aveUtility[index-10] / aveUtility[index]
            print(check)
            if check > 0.99: break

        # sort new generation
        newGen.sort(key= lambda u: u.utility)

        # assign working generation to new generation
        currentGen = newGen

        # output new generation utility to console and file
        file.write("Gen {}:\taveUtil = {}\n".format(i+1, getGenUtilAve(newGen)))
        print("Gen {}:\taveUtil = {}".format(i, getGenUtilAve(newGen)))

    # plotting average utility by generation
    plt.plot(aveUtility)
    plt.ylabel('Average Utility'), plt.xlabel('Generation')
    plt.show()

    # output info on max utility solution
    print("max Utility = {}, weight = {}".format(maxUtility.utility, maxUtility.weight))
    print("max Utility knapsack : \n", maxUtility.knapsack)
    file.write("max Utility = {}, weight = {}".format(maxUtility.utility, maxUtility.weight))
    file.write("max Utility knapsack \n:{}".format(maxUtility.knapsack))
    file.close()
