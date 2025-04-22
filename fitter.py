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

    def __init__(self,path):
        self.pipe = Pipeline(debug=False)
        fields = ['OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars', 'zAltPars']
        self.preProcess = Database("preProcess",fields,path)

    def fitFile(self, filePath, spec):
        obj_nme = basename(filePath)
        l2 = self.preProcess.getByName(obj_nme)
        if l2 == []:
            l2_product = get_all_fits(self.pipe,str(filePath), spec)
            self.preProcess.addByName(obj_nme,l2_product)
        else:
            l2_product = l2#convert_l2(l2)

        return l2_product

    def populate(self, files, directory):
        for file in files:
            path=Path(directory) / file
            spectra = tool.SDSS_spectrum(path) 
            fitting = self.fitFile(Path(directory) / file,spectra)
    def getBestGuess(self):
        return self.bestdatabase

    