from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from models.genetic.chromosome.Chromosome import Chromosome
from models.genetic.chromosome.GeneticChromosome import GeneticChromosome
from models.genetic.chromosome.analyzeInfoConfig import AnalyzeInfoConfig
import numpy as np

from abc import ABC, abstractmethod
import matplotlib
import webcolors
import math
from models.genetic.chromosome.Distribution import Distribution

class Color(GeneticChromosome):

    def __init__(self):
        super().__init__()
        self.__averageColorList = [] # [0,0,0] list of rgb
        self.__representationTable = None #Distribution type

    @staticmethod
    def colorDifference(color_rgb_1, color_rgb_2):
        rgb1 = sRGBColor(color_rgb_1[0], color_rgb_1[1], color_rgb_1[2])
        rgb2 = sRGBColor(color_rgb_2[0], color_rgb_2[1], color_rgb_2[2])
        color_lab_1 = convert_color(rgb1, LabColor)
        color_lab_2 = convert_color(rgb2, LabColor)
        d = delta_e_cie2000(color_lab_1, color_lab_2)
        return d

    def analyzeDistributionList(self, colorList, flowerNumber):
        
        for colorPixel in colorList:
            self.__averageColorList.append([colorPixel.getRGB(),colorPixel.getQuantity(),flowerNumber,colorPixel.getIdealDiference()])

    def createDistributionTable(self, avergeColorList, numElements, binaryRepresentation):
        # Average color list compostion: [RGB Subgroup, times it appears, currentFlower,   ((x)) currentDifference]
        # distributionTable : [RGB Subgroup, Distribution]
        minimun = 0
        distributionTable = []
        currentDistribution = None
        for color in avergeColorList:
            # Set distribution
            currentDistribution = Distribution()
            currentDistribution.setTotal(binaryRepresentation)
            currentDistribution.setQuantity(color[1]) # color size
            currentDistribution.setPercentage(numElements) # %
            currentDistribution.setRange(minimun) 
            minimun = math.floor((currentDistribution.getRangeMax())) + 1
            if(color is avergeColorList[-1]):
                currentDistribution.setMaxRange(binaryRepresentation)
            # Append to distribution table
            distributionTable.append([color[0], currentDistribution])
        return distributionTable



    #define abstract method
    def analyzeDistribution(self, flowerPartPixels, flowerPartImageInfo): #Como creo la tabla de distribucion para los coleres
        print("analyze COLOR")
        floweNumber = 0
        numElements = 0
        for colorList in flowerPartPixels:
            #Store data in variable self.__averageColorList
            self.analyzeDistributionList(colorList, floweNumber)
            for colorPixels in colorList:
                numElements += colorPixels.getQuantity()
            floweNumber += 1

        #Create a distribution table 
        #print(numElements)     
        self.__representationTable = self.createDistributionTable(self.__averageColorList, numElements, 65535) #Numero magico  
        for element in self.__representationTable:
           print("Color:", element[0], end=" ")
           element[1].print()

        self.setAnalyzeInfo()
        return self.analyzeInfo

    def setAnalyzeInfo(self):
        images = [] #array
        index = 1
        images.append([np.zeros([1000, 1000, 3], dtype=np.uint8), "Colors"]) #images[0]
        distributionTemp = self.__representationTable
        paintDistribution = []
        totalLength = 1000 * 1000

        for element in distributionTemp:
            paintDistribution.append([element[0],math.floor(totalLength * element[1].getPercentage() / 100)])
            print(element[0], " Cantidad para llenar imagen: ",totalLength * element[1].getPercentage())

        paintDistributionIndx = 0

        # Fill with color      
        for x in range(0,1000):
            for y in range(0, 1000):
                if(paintDistributionIndx < len(paintDistribution) - 1 and paintDistribution[paintDistributionIndx][1] <= 0):
                    print(paintDistribution[paintDistributionIndx][1])
                    print('PAIN')
                    paintDistributionIndx += 1
                images[0][0][y][x] = paintDistribution[paintDistributionIndx][0] #Blue
                paintDistribution[paintDistributionIndx][1] -= 1
                
                

        self.analyzeInfo[AnalyzeInfoConfig.DESCRIPTION] = "Colores del "
        self.analyzeInfo[AnalyzeInfoConfig.IMAGES] = images


    #Define abstract method
    def fitness(self):
        pass
