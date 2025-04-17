
from xpca.pipeline import Pipeline
from database_csv import Database
import numpy as np

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )

from handler_xpca import get_all_fits

class Fitter:

    pipe: Pipeline
    preProcess: Database
    best : str
    redshift: float
    layout: QVBoxLayout
    templateInfo: QLabel

    def __init__(self):
        self.pipe = Pipeline(debug=False)
        fields = ['OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars', 'zAltPars']
        self.preProcess = Database("preProcess",fields)

    def fitFile(self, filePath, spec):
        obj_nme = filePath[-21:][:-5]
        l2 = self.preProcess.getFitting(obj_nme)
        if l2 == []:
            #self.pipe.run(filePath, source='sdss')
            l2_product = get_all_fits(self.pipe,filePath, spec)
            self.preProcess.addFitting(l2_product)
            #print(self.pipe.full_results)
        else:
            l2_product = convert_l2(l2)

        return l2_product

    def getBestGuess(self):
        return self.best
        return self.l2_product


def convert_l2(row):
    l2_product = dict()
    l2_product['OBJ_NME']       = row['OBJ_NME']
    l2_product['zBest']         = float(row['zBest'])
    l2_product['zBestProb']     = float(row['zBestProb'])
    l2_product['zBestType']     = row['zBestType']
    l2_product['zBestSubType']  = row['zBestSubType']
    
    def auxInsert(temp,i,new):
        x = temp[i]
        if x != '--':
            new.insert(i,  x.strip("'")) 
    
    def auxInsertFloat(temp,i,new):
        x = temp[i]
        if x != '--':
            new.insert(i,  float(x.strip(','))) 

    def aux(key, func):
        temp = row[key].strip('[]').split()
        new = []
        for i in range(len(temp)):
            func(temp,i,new)
        return new

    l2_product['zAltType'] = aux('zAltType',lambda temp,i,new: new.insert(i,  temp[i].strip("'")))

    l2_product['zAltSubType'] = aux('zAltSubType',auxInsert)

    l2_product['zAltProb'] = aux('zAltProb',auxInsertFloat)

    l2_product['zBestPars'] = np.array(aux('zBestPars',lambda temp,i,new: new.insert(i, float(temp[i].strip(',')))))
    return l2_product