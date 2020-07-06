from models.genetic.algorithm.individual import Individual
from operator import attrgetter

class Population:

    def __init__(self):
        self.individuals = [] #obj Individual List 

    #Generate inicial population
    def generatePopulation(self, popSize):
        for i in range(0, popSize):
            self.individuals.append(Individual())

    def purgePopulation(self, deadRate):
        self.sortPopulation()
        deletePoint = int(len(self.individuals) * ((100-deadRate)/100))

        print("--SELECT POPULATION--")
        print("Delete point: " + str(deletePoint))
        #self.printPopulation()
        del self.individuals[deletePoint:]



    #Sort population by fitness
    def sortPopulation(self):
        self.individuals = sorted(self.individuals, key=attrgetter('fitness'))

    def getIndividual(self, index):
        return self.individuals[index]

    def addOffsprings(self, offsprings):
        self.individuals.extend(offsprings)

    #Simple test print
    def printPopulation(self):
        individualNum = 0
        for individual in self.individuals:
            print('INDIVIDUAL NUMBER #',individualNum)
            print('Individual genes: ', individual.getGene())
            print('Individual fitness: ', individual.getFitness())
            individualNum += 1
