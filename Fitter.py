from xpca.pipeline import Pipeline
from CSVDatabase import Database
import Spec_tools as tool
from DataObject import DataObject

from PySide6.QtCore import (
    QObject,
    QDir,
    Signal,
)

"""
This class interfaces with XPCA and is responisble for retrieving fittings which are used to draw the template over the graph
"""
class Fitter(QObject):

    pipe: Pipeline
    preProcess: Database
    best : str
    redshift: float
    fileFitted = Signal(int)

    def __init__(self, database):
        QObject.__init__(self)
        self.pipe = Pipeline(debug=False)
        self.preProcess = database

    def loadDataObject(self, itempath, filename):
        spectra = tool.SDSS_spectrum(itempath)
        l2 = self.preProcess.getFitting(filename)
        return DataObject(filename, spectra, l2, itempath)  

    def openFiles(self, path):
        self.pipe.run(path, source='sdss')
        directory = QDir(path)
        directory.setNameFilters(['([^.]*)','*.fits'])
        files = directory.entryList()
        pairs = [(files[i], self.pipe.catalog_items[i]) for i in range(len(files))]
        for pair in pairs:
            self.preProcess.addFitting(pair[0], pair[1])

    def populate(self, objs, N=0):
        counter = 0
        for obj in objs:
            if counter < N:
                if obj.fitting is None:
                    counter = counter+1
                    obj = self.fitFile(obj.path,obj)
                    self.fileFitted.emit(counter)
            else:
                break
        return objs

    def fitFile(self, path, dataObj=None):
        if dataObj is None:
            dataObj = self.loadDataObject(path)
        if dataObj.fitting is None:
            self.pipe.N_targets = 1
            self.pipe.run(str(dataObj.path), source='sdss')
            dataObj.fitting = self.pipe.catalog_items[0]
            self.preProcess.addFitting(dataObj.name, dataObj.fitting)
        dataObj.category = dataObj.fitting['zBestSubType']
        dataObj.redshift = dataObj.fitting['zBest']

        return dataObj