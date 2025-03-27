
from xpca.pipeline import Pipeline
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )

class Fitter:

    pipe: Pipeline
    l2_product: dict
    best : str
    redshift: float
    layout: QVBoxLayout
    templateInfo: QLabel

    def __init__(self):
        self.pipe = Pipeline()
        self.layout = QVBoxLayout()

    def fitFile(self, filePath):
        self.clearLayout()
        self.pipe.run(filePath, source='sdss')
        l2_product = self.pipe.catalog_items[0]
        self.l2_product = l2_product

        ZBEST  = self.l2_product['zBest']
        self.redshift = ZBEST
        self.best = l2_product['zBestSubType']
        self.layout.addWidget(QLabel("template: " + self.best + ': %.5f' % ZBEST))

        self.layout.addWidget(QLabel("Class, Probability"))

        classification = l2_product['zBestSubType']
        probability    = l2_product['zBestProb'] * 100

        self.layout.addWidget(QLabel(classification + ': %.2f %%' % probability))

        for i in range(len(l2_product['zAltSubType'])):
            probability = l2_product['zAltProb'][i] * 100
            if probability > 10:
                text = l2_product['zAltSubType'][i] + ': %.2f %%' % probability
                self.layout.addWidget(QLabel(text))

    def getBestGuess(self):
        return self.best

    def getl2_product(self):
        return self.l2_product
    
    def clearLayout(self):
        for i in range(self.layout.count()): self.layout.itemAt(i).widget().close()