
from xpca.pipeline import Pipeline
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )

class Fitter:

    pipe: Pipeline
    l2_product: dict
    best : str
    layout: QVBoxLayout
    templateInfo: QLabel

    def __init__(self):
        self.pipe = Pipeline()
        self.layout = QVBoxLayout()

    def fitFile(self, filePath):
        self.clearLayout()
        self.pipe.run(filePath, source='sdss')
        self.l2_product = self.pipe.catalog_items[0]

        ZBEST  = self.l2_product['zBest']
        self.best = self.l2_product['zBestSubType']
        self.layout.addWidget(QLabel("template: " + self.best + ': %.5f' % ZBEST))

        self.layout.addWidget(QLabel("Class, Probability"))

        classification = self.l2_product['zBestSubType']
        probability    = self.l2_product['zBestProb'] * 100

        self.layout.addWidget(QLabel(classification + ': %.2f %%' % probability))

        for i in range(len(self.l2_product['zAltSubType'])):
            probability = self.l2_product['zAltProb'][i] * 100
            if probability > 10:
                text = self.l2_product['zAltSubType'][i] + ': %.2f %%' % probability
                self.layout.addWidget(QLabel(text))

    def getBestGuess(self):
        return self.best

    def getl2_product(self):
        return self.l2_product
    
    def clearLayout(self):
        for i in range(self.layout.count()): self.layout.itemAt(i).widget().close()