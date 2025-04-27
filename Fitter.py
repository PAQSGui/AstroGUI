from xpca.pipeline import Pipeline
from CSVDatabase import Database
import numpy as np
import Spec_tools as tool
from pathlib import Path
from os.path import basename

from DataObject import DataObject

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )

from xpcaWidget import get_all_fits, createTarget

import Spec_tools as tool
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

    def __init__(self, database):
        self.pipe = Pipeline(debug=False)
        fields = ['OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars', 'zAltPars']
        self.preProcess = database

    def populate(self, files, path):
        objs = []
        for file in files:
            spectra = tool.SDSS_spectrum(path / file) 
            obj = self.fitFile(str(path / file),spectra)
            dict = obj.toDict()
            objs.append(obj)
        return objs

    def fitFile(self, path, spectra, dataObj=None):
        if dataObj is None:
            obj_nme = path[-21:][:-5]
            l2 = self.preProcess.getFitting(obj_nme)
            dataObj=DataObject(obj_nme,spectra,l2,path)
        filePath = Path(path)# / Path(dataObj.name)
        l2 = self.preProcess.getFitting(dataObj.name)
        if l2 is None:
            self.pipe.N_targets=1
            dataObj.fitting = self.pipe.process_target(createTarget(str(filePath),dataObj.file), 0)[0]
            self.preProcess.addFitting(dataObj.fitting)
        else:
            dataObj.fitting = l2
        dataObj.category = dataObj.fitting['zBestSubType']
        dataObj.redshift = dataObj.fitting['zBest']

        return dataObj

    def getBestGuess(self):
        return self.bestdatabase

    