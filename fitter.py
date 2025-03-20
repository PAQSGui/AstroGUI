
from xpca.pipeline import Pipeline

class Fitter:

    pipe: Pipeline

    info_2xp : str
    info_2cp : str

    def __init__(self):
        self.pipe = Pipeline()

        self.info_2xp = "2XP: best-fit template + Z\_BEST (plus lines)"
        self.info_2cp = "2CP: CLASS, PROB, CLASS2, PROB2"

    def fitFile(self, filePath):
        self.pipe.run(filePath,source='sdss')
        ZBEST=self.pipe.catalog_items[0]['zBest']
        CLASS=self.pipe.catalog_items[0]['zBestSubType']
        PROB=self.pipe.catalog_items[0]['zBestProb']
        self.info_2xp.setText("2XP: best-fit template + "+ str(ZBEST) +" (plus lines)")
        self.info_2cp.setText("2CP: "+ CLASS +", "+ str(PROB) +", CLASS2, PROB2")