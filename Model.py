from Fitter import Fitter
from CSVDatabase import Database
from DatabaseUtility import getdataModelFromDatabase
from os.path import dirname
import DataObject

from PySide6.QtCore import (
    QObject,
    Signal,
    QDir,
)

import Spec_tools as tool
from pathlib import Path

"""
Model interfaces between the UI elements and the databases
It also maintains a dictionary of 'options', which are used to change behaviours in the program
Any new options should be added to the dictionary and only accesed with the methods
"""
class Model(QObject):
    cursor = 0
    objects = []
    options: dict
    l2FieldNames = ['name', 'OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars', 'zAltPars']
    
    objFieldNames = ['name','categorized', 'category', 'redshift', 'note']
    validationDB : Database
    fitter: Fitter

    openedSession = Signal(list)
    closedSession = Signal(list)
    xpcaDone = Signal(int)

    def openFiles(self, files):
        path = dirname(files)
        if len(files)==0:
            return
        self.path = path
        self.closedSession.emit(files)
        self.startup()        
        self.objects = self.getEmptydataModel(files)

        self.initOptions()
        self.openedSession.emit(files)

    def openFolder(self, path):
        directory = QDir(path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()[0:5] #Currently only analyses the first 5 elements
        if len(files)==0:
            raise FileNotFoundError("Folder '%s' does not contain any FITS files" %path)
        self.path = path
        self.closedSession.emit(path)
        self.startup()
        self.objects = self.getEmptydataModel(files)

        self.initOptions()
        self.openedSession.emit(files)

    def startup(self):
        self.validationDB = Database('validation', self.objFieldNames, self.path)
        preProcess = Database("preProcess",self.l2FieldNames, self.path)
        self.fitter = Fitter(preProcess)   

    def getEmptydataModel(self,files):
        objs=[]
        try: #replace with typecheck
            for item in list(files):
            
                dataModel=getdataModelFromDatabase(self.path / Path(item),self.fitter.preProcess)
                for name in list(dataModel.keys()):
                    spectra = tool.SDSS_spectrum(self.path / Path(name))
                    objs.append(DataObject.DataObject(name, spectra, dataModel[name]))
            return objs
        except UnicodeDecodeError:
                
            return self.fitter.populate(files, Path(self.path))   

    def updateCursor(self, delta):
        self.cursor = self.cursor + delta
        if self.cursor<0:
            self.cursor=len(self.objects)-1
        elif self.cursor>=len(self.objects):
            self.cursor=0

    def setOption(self, opt, val):
        self.options[opt] = val
    
    def changeRedShift(self, val):
        self.objects[self.cursor].changeRedshift(val)
    
    def changeCategory(self, cat):
        self.objects[self.cursor].changeCategory(cat) 

    def getOption(self, opt):
        return self.options[opt]
    
    def getOptions(self):
        return self.options

    def getRedShift(self):
        obj=self.objects[self.cursor]
        if obj.fitting is not None:
            return float(self.objects[self.cursor].redshift)
        else:
            return 0
    
    def getCategory(self):
        obj=self.objects[self.cursor]
        if obj.fitting!=None:
            return self.objects[self.cursor].category
        else:
            return ""
    
    def getState(self):
            return self.objects[self.cursor]

    def getFile(self):
        return self.objects[self.cursor].file

    def addDBEntry(self, categorised, note):
        object = self.objects[self.cursor]

        if categorised:
            category = object.category
            redshift = object.redshift
        else:
            category = None
            redshift = None

        if note == '':
            note = 'no-note'

        self.validationDB.addEntry(self.objFieldNames, [object.name, categorised, category, redshift, note])

    def getDBEntry(self, name):
        row = self.validationDB.getEntry(name,None)
        if row is not None:
            return row
        return None
    
    def getNote(self):
        name = self.getState().name
        entry = self.getDBEntry(name)
        if entry is not None:
            return entry['note']
        return ""

    def initOptions(self):
        options = {
            'LineWidth': 0.5,
            'GraphColor': 'Black',
            'TemplateColor' : 'Red',
            'NoiseColor' : 'Grey',
            'SNColor': 'Blue',
            'SkyColor': 'Orange',
            'ShowSN' : False,
            'ShowSky' : False,
            'yLimit' : False,
            'ymin' : 0,
            'ymax' : 0,
            'zResolution' : 1e4,
            'zMax' : 6,
            'zMin' : 0,
            }
        self.options = options

    def resetYLimit(self):
        self.options['yLimit'] = False
        self.options['ymin'] = 0
        self.options['ymax'] = 0