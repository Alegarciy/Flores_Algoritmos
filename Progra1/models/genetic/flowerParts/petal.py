from models.genetic.flowerParts.flowerPart import FlowerPart
from models.genetic.flowerParts.flowerPartConfig import FlowerPartConfig
from models.converter.flowerConfig import FlowerConfig

class Petal(FlowerPart):
    def __init__(self):
        #LLama al constructor de la clase FlowerPart
        super().__init__(FlowerPartConfig.PETAL)
        self.quantity = 0

    #Toma los datos necesarios para hacer el analisis del petalo
    def setFlowerPartImages(self, flowerImages):
        for flower in flowerImages:
            self.flowerPartPixels.append(flower.getPetalPixels())
            jsonInfo = flower.getJsonData()
            info =\
                {
                    FlowerPartConfig.PIXEL_CENTRAL: jsonInfo[FlowerConfig.PIXEL_CENTRAL],
                    FlowerPartConfig.FLOWERPART_LIMIT: jsonInfo[FlowerConfig.PIXEL_PETAL_LIMIT],
                    FlowerPartConfig.FLOWERPART_OUTLINE_INIT_POS: jsonInfo[FlowerConfig.PETAL_OUTLINE_INIT_POS],
                    FlowerPartConfig.FLOWERPART_OUTLINE_END_POS: jsonInfo[FlowerConfig.PETAL_OUTLINE_END_POS],
                    FlowerPartConfig.FLOWERPART_OUTLINE_INCREASE: jsonInfo[FlowerConfig.PETAL_OUTLINE_INCREASE],
                    FlowerPartConfig.QUANTITY_FLOWERPART: jsonInfo[FlowerConfig.CTD_PETALOS],
                    FlowerPartConfig.FLOWERPART_OUTLINE_AXIS: jsonInfo[FlowerConfig.PETAL_OUTLINE_AXIS]
                }
            self.flowerPartImageInfo.append([flower.getPetal(), info])

    #Analiza el promedio de la cantidad de petalos
    def analyzeQuantityOfPetals(self):
        self.quantity = 0
        for flowerInfo in self.flowerPartImageInfo:
            info = flowerInfo[1]
            self.quantity += info[FlowerPartConfig.QUANTITY_FLOWERPART]
        self.quantity = int(self.quantity/len(self.flowerPartImageInfo))


    def analyzeChromosome(self, chromosome):
        analysisInfo = self.chromosomes[chromosome].analyzeDistribution\
        (
            self.flowerPartPixels,
            self.flowerPartImageInfo,
            self.description
        )

        self.analyzeQuantityOfPetals()
        return analysisInfo