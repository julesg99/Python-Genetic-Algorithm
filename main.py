import numpy

popSize = 1000
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


# generation is a list of 1000 different solutions
generation = []
for i in range(0, popSize):
    weight = 0
    list = []
    while weight < 500:
        temp = numpy.random.randint(0, 400)
        list.append(gear[temp])
        weight += gear[temp][1]
    generation.append(list)

print(generation)

scores = []
for i in range(0, popSize):
    totalUtil = 0
    for j in range(0, len(generation[i])):
        totalUtil += generation[i][j]

print(scores)





                                # popSize = (1000, 1000)
# generation = numpy.random.randint(0, 401, popSize)
# print(generation)

# for i in range(0, len(generation)):
#     weight = 0
#     for j in range(0, len(generation[i])):
#         weight += gear[generation[i][j]][1]
#     print(weight/20)



# a generation is presented as a list of integers, each value ranging from 0-400
# each integer represents an index location in the gear list
# building first generation
# gen1 = []
# weight = 0
# for i in range(0, popSize[0]):
#     gen1.append(random.randint(0, len(gear)-1))
#     print(gear[gen1[i]][1])
#     weight += gear[gen1[i]][1]
# weight /= 20
# print(weight)


class solution:
    gear =[]




