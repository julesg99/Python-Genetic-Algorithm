import numpy


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
        print("solution = ", self.knapsack, "\nlength = ", len(self.knapsack), "\ntotal weight = ", self.totalWeig, "\ntotal utility = ", self.totalUtil, "\n")

    # constructor for creating a solution based on two parents
    # def __int__(self, parents):
    #     population = []
    #
    # def mutation(self):
    #     # stuff
    #
    # def selection(self):
    #     # stuff
    #
    #     # necessary?
    # def crossover(self):
    #     # stuff

# number of combinations
popSize = 5
# likelihood of a mutation happening
muteRate = 0.0001

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


# attempting to create a generation of 1000 combinations
generation = list()
for i in range(popSize):
    generation.append(Solution(gear))



