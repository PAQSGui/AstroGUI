
from xpca.pipeline import Pipeline

class Fitter:

    pipe: Pipeline
    l2_product: dict
    best : str
    info_2xp : str
    info_2cp : str

    def __init__(self):
        self.pipe = Pipeline()

        self.info_2xp = "2XP: best-fit template + Z\_BEST (plus lines)"
        self.info_2cp = "2CP: CLASS, PROB, CLASS2, PROB2"

    def fitFile(self, filePath):
        self.pipe.run(filePath, source='sdss')
        self.l2_product=self.pipe.catalog_items[0]
        ZBEST=self.l2_product['zBest']
        CLASS=self.l2_product['zBestSubType']
        PROB=self.l2_product['zBestProb']
        self.best = str(ZBEST) + '-' + str(CLASS)
        self.info_2xp = "2XP: best-fit template + "+ str(ZBEST) +" (plus lines)"
        self.info_2cp = "2CP: "+ CLASS +", "+ str(PROB) +", CLASS2, PROB2"

    def getBestGuess(self):
        return self.best

    def getl2_product(self):
        return self.l2_product