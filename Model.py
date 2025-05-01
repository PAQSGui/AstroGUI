from Fitter import Fitter
from CSVDatabase import Database
import os.path

from PySide6.QtCore import (
    QObject,
    Signal,
    QDir,
)

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
    
    objFieldNames = ['name', 'categorized', 'category', 'redshift', 'note']
    validationDB : Database
    fitter: Fitter

    opened = False
    openedSession = Signal(int)
    closedSession = Signal(int)

    def openFolder(self, path):
        directory = QDir(path)
        directory.setNameFilters(['([^.]*)','*.fits'])
        files = directory.entryList()[0:100]
        if len(files) == 0:
            raise FileNotFoundError(f'Folder {path} does not contain any FITS files')  
        self.path = path
        self.startup()
        self.objects = self.setupDataModel(files)
        self.initOptions()

        if self.opened:
            self.closedSession.emit(1)
        self.openedSession.emit(1)
        self.opened = True

    def startup(self):
        self.validationDB = Database('validation', self.objFieldNames, self.path)
        preProcess = Database('preProcess',self.l2FieldNames, self.path)
        self.fitter = Fitter(preProcess)   

    def setupDataModel(self, files):
        objs = []
        for item in list(files):
            itempath = os.path.join(self.path, item)
            dataObj = self.fitter.loadDataObject(itempath, item)
            objs.append(dataObj)
        return objs

    def updateCursor(self, delta):
        self.cursor = self.cursor + delta
        if self.cursor < 0:
            self.cursor = len(self.objects)-1
        elif self.cursor >= len(self.objects):
            self.cursor = 0

    def setOption(self, option, value):
        self.options[option] = value

    def getOption(self, option):
        return self.options[option]    

    def getOptions(self):
        return self.options
    
    def changeRedShift(self, value):
        self.objects[self.cursor].changeRedshift(value)
    
    def changeCategory(self, category):
        self.objects[self.cursor].changeCategory(category) 

    def getRedShift(self):
        obj = self.objects[self.cursor]
        if obj.fitting is not None:
            return float(self.objects[self.cursor].redshift)
        else:
            return 0
    
    def getCategory(self):
        obj = self.objects[self.cursor]
        if obj.fitting is not None:
            return self.objects[self.cursor].category
        else:
            return ''
    
    def getState(self):
        return self.objects[self.cursor]

    def addDBEntry(self, categorised, note):
        dataObject = self.objects[self.cursor]

        if categorised:
            category = dataObject.category
            redshift = dataObject.redshift
        else:
            category = None
            redshift = None

        if note == '':
            note = 'no-note'

        self.validationDB.addEntry(self.objFieldNames, [dataObject.name, categorised, category, redshift, note])

    def getDBEntry(self, name):
        row = self.validationDB.getEntry(name, None)
        return row
    
    def getNote(self):
        name = self.getState().name
        entry = self.getDBEntry(name)
        if entry is not None:
            note = entry['note']
            if note != 'no-note':
                return note
        return ''

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