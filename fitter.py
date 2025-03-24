
from xpca.pipeline import Pipeline
from PySide6.QtWidgets import (
    QLabel,
    )

class Fitter:

    pipe: Pipeline
    l2_product: dict
    best : str
    info_2xp : QLabel
    info_1cp : QLabel
    info_2cp : QLabel
    info1 : QLabel

    def __init__(self):
        self.pipe = Pipeline()

        self.info_2xp = QLabel()
        self.info_1cp = QLabel()
        self.info_2cp = QLabel()
        self.info1 = QLabel("testing") 

    def fitFile(self, filePath):
        self.pipe.run(filePath, source='sdss')
        self.l2_product = self.pipe.catalog_items[0]
        ZBEST  = self.l2_product['zBest']
        CLASS  = self.l2_product['zBestSubType']
        PROB   = self.l2_product['zBestProb'] * 100
        CLASS2 = self.l2_product['zAltSubType'][0]
        PROB2  = self.l2_product['zAltProb'][0] * 100
        self.best = str(CLASS)
        self.info_2xp.setText(CLASS + ": " + str(ZBEST) +" (plus lines)")
        self.info_1cp.setText(CLASS + ', %.2f %%' % PROB)
        self.info_2cp.setText(CLASS2 + ', %.2f %%' % PROB2)

        self.info1.setText("updated")

    def getBestGuess(self):
        return self.best

    def getl2_product(self):
        return self.l2_product