
from xpca.pipeline import Pipeline
from database import Database
import numpy as np
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )
from PySide6.QtGui import (
    Qt,
)

class Fitter:

    pipe: Pipeline
    database: Database
    best : str
    redshift: float
    layout: QVBoxLayout
    templateInfo: QLabel

    def __init__(self):
        self.pipe = Pipeline()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        fields = ['OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars']
        self.database = Database("preProcess.csv",fields)

    def fitFile(self, filePath):
        obj_nme = filePath[-21:][:-5]
        l2 = self.database.getFitting(obj_nme)
        if l2 == []:
            self.pipe.run(filePath, source='sdss')
            l2_product = self.pipe.catalog_items[0]
            self.database.addFitting(l2_product)
        else:
            l2_product = convert_l2(l2)


        self.clearLayout()
        ZBEST  = float(l2_product['zBest'])
        self.redshift = ZBEST
        self.best = l2_product['zBestSubType']

        classification = l2_product['zBestSubType']
        probability    = l2_product['zBestProb'] * 100

        self.layout.addWidget(QLabel(classification + ': %.2f %%' % probability))

        subTypes = l2_product['zAltSubType']
        probabilities = l2_product['zAltProb']

        for i in range(1,len(subTypes)):
            probability = probabilities[i] * 100
            if probability > 10:
                text = subTypes[i] + ': %.2f %%' % probability
                self.layout.addWidget(QLabel(text))

        return l2_product

    def getBestGuess(self):
        return self.best

    def getl2_product(self, name):
        return self.l2_product
    
    def clearLayout(self):
        for i in range(self.layout.count()): self.layout.itemAt(i).widget().close()

def convert_l2(row):
    l2_product = dict()
    l2_product['OBJ_NME']       = row['OBJ_NME']
    l2_product['zBest']         = float(row['zBest'])
    l2_product['zBestProb']     = float(row['zBestProb'])
    l2_product['zBestType']     = row['zBestType']
    l2_product['zBestSubType']  = row['zBestSubType']

    tempAltType = row['zAltType'].strip('[]').split()
    newAltType = []
    for i in range(len(tempAltType)):
        newAltType.insert(i,  tempAltType[i].strip("'"))
    l2_product['zAltType'] = newAltType

    tempAltSubType = row['zAltSubType'].strip('[]').split()
    newAltSubType = []
    for i in range(len(tempAltSubType)):
        subType = tempAltSubType[i]
        if subType != '--':
            newAltSubType.insert(i,  subType.strip("'")) 
    l2_product['zAltSubType'] = newAltSubType

    tempAltProb = row['zAltProb'].strip('[]').split()
    newAltProb = []
    for i in range(len(tempAltProb)):
        prob = tempAltProb[i]
        if prob != '--':
            newAltProb.insert(i, float(prob.strip(',')))
    l2_product['zAltProb'] = newAltProb

    tempBestPars = row['zBestPars'].strip('[]').split()
    newBestPars = []
    for i in range(len(tempBestPars)):
        newBestPars.insert(i, float(tempBestPars[i].strip(',')))
    l2_product['zBestPars'] = np.array(newBestPars)

    return l2_product
