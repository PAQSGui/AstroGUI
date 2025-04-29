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

from PySide6.QtCore import (
    QDir,
)

from xpcaWidget import get_all_fits, xpcaWindow, createTarget

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
        self.preProcess = database

    def loadDataObject(self, itempath):
        spectra = tool.SDSS_spectrum(itempath) 
        obj_nme = str(itempath)[-21:][:-5]
        l2 = self.preProcess.getFitting(obj_nme)
        return DataObject(obj_nme,spectra,l2,itempath)  

    def openFiles(self,path):
        self.pipe.run(path,source='sdss')
        directory = QDir(path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()
        pairs=[(files[i],self.pipe.catalog_items[i]) for i in range(len(files))]
        for x in pairs:
            self.preProcess.addFitting(x[0], x[1])

    def populate(self, path, files=None, objs=[], N=-1):
        if objs == []:
            for file in files:
                if N!=0:
                    obj = loadDataObject(self, itempath)
                    if obj.fitting is None:
                        N=N-1
                    obj = self.fitFile(obj.path,obj)
                    objs.append(obj)
                else:
                    break
        else:
            for obj in objs:
                if N!=0:
                    if obj.fitting is None:
                        N=N-1
                    obj = self.fitFile(obj.path,obj)
                else:
                    break
        return objs

    def fitFile(self, path, dataObj=None):
        if dataObj is None:
            dataObj=loadDataObject(self, path)
        if dataObj.fitting is None:
            self.pipe.N_targets=1
            dataObj.fitting = self.pipe.process_target(createTarget(dataObj.path,dataObj.file), 0)[0]
            self.preProcess.addFitting(dataObj.name, dataObj.fitting)
        dataObj.category = dataObj.fitting['zBestSubType']
        dataObj.redshift = dataObj.fitting['zBest']

        return dataObj

    def getBestGuess(self):
        return self.bestdatabase

    