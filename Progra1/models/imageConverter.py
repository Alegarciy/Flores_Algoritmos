#import cv2
from matplotlib import pyplot as plt
import numpy as np
from skimage import io
import io as i_o
import base64
from models.config import Config
from models.fileManager import FileManager
from models.flowerImage import FlowerImage
from models.flowerConfig import FlowerConfig
from models.genetic.chromosome.color import Color
class ImageConverter:

    def __init__(self):
        self.userImages = []
        self.I = 0
        self.J = 1
        self.imageIndex = 0
        self.progress = 0
        self.isRunning = False
        self.finished = False

    def isReadyToConvert(self):
        if(len(self.userImages)  >= 1 and not self.isRunning):
            return True
        return False


    def addImage(self, image, jsonData, filename, extension):
        numberFlower = len(self.userImages)
        flowerDirectory = Config.DATADIRECTORY + "/" + filename
        #Save Flower image

        flowerFilename = Config.IMAGEFILENAME + "." + extension
        FlowerImagePathBackEnd = FileManager.save_image(image, flowerDirectory, flowerFilename)

        flowerFolder = Config.STATICFOLDER + "/" + Config.USERINPUTFOLDER + "/" + filename
        flowerImagePathFrontEnd = flowerFolder + "/" + flowerFilename

        #Save Json Data
        jsonFilename = Config.JSONFILENAME + Config.JSONEXTENSION
        FileManager.save_json(jsonData, flowerDirectory, jsonFilename)

        #Read
        jsonDirectory = flowerDirectory + "/" + jsonFilename
        json = FileManager.read_json(jsonDirectory)

        #Transform image in Numpy.array
        image = io.imread(FlowerImagePathBackEnd)

        flowerDirectory.replace("/", "\\")
        #Create flowerImage instance
        flowerImage = FlowerImage(image, flowerImagePathFrontEnd, FlowerImagePathBackEnd, json, flowerDirectory, filename)

        #Add flower image to userInput list
        self.userImages.append(flowerImage)

        self.finished = False

    def deleteImage(self, position):
        flower = self.userImages[position]
        FileManager.removeDirectory(flower.getFlowerDirectory())
        self.userImages.remove(flower)
        self.finished = False

    #Recorre las imagenes del usuario (numpy arrays) y llama al voraz

    def convert(self):
        self.isRunning = True
        self.imageIndex = 0
        for flowerImage in self.userImages:
            self.convertImage(flowerImage)
            self.imageIndex += 1

        if(self.imageIndex>=len(self.userImages)>0):
            self.finished = True
        else:
            self.finished = False
        self.isRunning = False


    #Algoritmo voraz

    def convertImage(self, flowerImage):
        info = flowerImage.getJsonData()
        flowerPixels = flowerImage.getFlower() #Subestructura
        size_i = flowerImage.getSize_I()
        size_j = flowerImage.getSize_J()
        for i in range(0,size_i-1):
            print("isRunning")
            for j in range(0, size_j-1):
                self.progress = ((i*size_i + (j+1)) / (size_i*size_j))*100
                if(self.isInCenter(i,j,info)):
                    if(self.isCenterColor(flowerPixels[i,j], info)):
                        center = flowerImage.getCenter()
                        center[i,j] = flowerPixels[i,j]
                elif(self.isInPetal(i,j,info)):
                    if(self.isPetalColor(flowerPixels[i,j], info)):
                        petal = flowerImage.getPetal()
                        petal[i,j] = flowerPixels[i,j]

    #Criterios

    def isInCenter(self, i, j, info):
        minI = info[FlowerConfig.PIXEL_CENTRAL][self.I] - info[FlowerConfig.PIXEL_CENTER_LIMIT][self.I]
        maxI = info[FlowerConfig.PIXEL_CENTRAL][self.I] + info[FlowerConfig.PIXEL_CENTER_LIMIT][self.I]
        minJ = info[FlowerConfig.PIXEL_CENTRAL][self.J] - info[FlowerConfig.PIXEL_CENTER_LIMIT][self.J]
        maxJ = info[FlowerConfig.PIXEL_CENTRAL][self.J] + info[FlowerConfig.PIXEL_CENTER_LIMIT][self.J]

        return (minI < i < maxI and minJ < j < maxJ)

    def isInPetal(self, i, j, info):
        minI = info[FlowerConfig.PIXEL_CENTRAL][self.I] - info[FlowerConfig.PIXEL_PETAL_LIMIT][self.I]
        maxI = info[FlowerConfig.PIXEL_CENTRAL][self.I] + info[FlowerConfig.PIXEL_PETAL_LIMIT][self.I]
        minJ = info[FlowerConfig.PIXEL_CENTRAL][self.J] - info[FlowerConfig.PIXEL_PETAL_LIMIT][self.J]
        maxJ = info[FlowerConfig.PIXEL_CENTRAL][self.J] + info[FlowerConfig.PIXEL_PETAL_LIMIT][self.J]

        return (minI < i < maxI and minJ < j < maxJ)

    def isPetalColor(self, pixel, info):
        return Color.colorDifference(pixel, info[FlowerConfig.COLOR_PETAL_PREF]) <= FlowerConfig.DIFFERENCE_COLOR_LIMIT

    def isCenterColor(self, pixel, info):
        return Color.colorDifference(pixel, info[FlowerConfig.COLOR_CENTER_PREF]) <= FlowerConfig.DIFFERENCE_COLOR_LIMIT

    def getConvertProcess(self):
        if(self.imageIndex >= len(self.userImages)):
            return "False"

        flowerImage = self.userImages[self.imageIndex]
        images = [flowerImage.getFlower(), flowerImage.getPetal(), flowerImage.getCenter()]
        titles = ["Flower", "Petal", "Center"]
        fig, axs = plt.subplots(1, 3, figsize=(7, 4), constrained_layout=True)
        for ax, image, title in zip(axs, images, titles):
            ax.imshow(image)
            ax.set_title(title)


        img = i_o.BytesIO()
        plt.savefig(img, format = "png")
        img.seek(0)
        base64_plot = base64.b64encode(img.getvalue()).decode()

        return base64_plot

    def getProgress(self):
        return str(int(self.progress))

