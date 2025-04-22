from xpca.pipeline import Pipeline
from database_json import Database
import numpy as np
import Spec_tools as tool
from pathlib import Path
from os.path import basename

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )

from handler_xpca import get_all_fits

"""
This class interfaces with XPCA and is responisble for retrieving fittings which are used to draw the template over the graph
"""
class Fitter:

    pipe: Pipeline
    preProcess: Database
    best : str
    redshift: float
    layout: QVBoxLayout
    templateInfo: QLabel

    def __init__(self,path, database):
        self.pipe = Pipeline(debug=False)
        fields = ['OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars', 'zAltPars']
        self.preProcess = database

    def fitFile(self, dataObj, path):
        filePath = Path(path) / Path(dataObj.name)
        l2 = self.preProcess.getByName(dataObj.name)
        if l2 == []:
            dataObj.fitting = get_all_fits(self.pipe,str(filePath), dataObj.file)
            self.preProcess.addByName(dataObj.name,dataObj.fitting)
        else:
            dataObj.fitting = l2
        dataObj.category = dataObj.fitting['zBestSubType']
        dataObj.redshift = dataObj.fitting['zBest']

        return dataObj

    def getBestGuess(self):
        return self.bestdatabase

    