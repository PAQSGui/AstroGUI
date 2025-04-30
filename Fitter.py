from xpca.pipeline import Pipeline
from CSVDatabase import Database
from xpcaWidget import createTarget
import Spec_tools as tool
from DataObject import DataObject

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    )

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
    layout: QVBoxLayout
    templateInfo: QLabel

    fileFitted = Signal(int)

    def __init__(self, database):
        QObject.__init__(self)
        self.pipe = Pipeline(debug=False)
        self.preProcess = database

    def loadDataObject(self, itempath, filename):
        spectra = tool.SDSS_spectrum(itempath)
        l2 = self.preProcess.getFitting(filename)
        return DataObject(filename, spectra, l2, itempath)  

    def openFiles(self,path):
        self.pipe.run(path, source='sdss')
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
                    obj = self.loadDataObject(path)
                    if obj.fitting is None:
                        N=N-1
                    obj = self.fitFile(obj.path,obj)
                    self.fileFitted.emit(1)
                    objs.append(obj)
                else:
                    break
        else:
            for obj in objs:
                if N!=0:
                    if obj.fitting is None:
                        N=N-1
                    obj = self.fitFile(obj.path,obj)
                    self.fileFitted.emit(1)
                else:
                    break
        return objs

    def fitFile(self, path, dataObj=None):
        if dataObj is None:
            dataObj = self.loadDataObject(path)
        if dataObj.fitting is None:
            self.pipe.N_targets=1
            dataObj.fitting = self.pipe.process_target(createTarget(dataObj.path,dataObj.file), 0)[0]
            self.preProcess.addFitting(dataObj.name, dataObj.fitting)
        dataObj.category = dataObj.fitting['zBestSubType']
        dataObj.redshift = dataObj.fitting['zBest']

        return dataObj
    