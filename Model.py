from fitter import Fitter
from database import Database, getdataModelFromDatabase
from os.path import dirname
import DataObject

from PySide6.QtCore import (
    QObject,
    Signal,
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
    fileFieldNames = ['name', 'file', 'category', 'redshift']
    l2FieldNames = ['OBJ_NME', 'zBest', 'zBestProb', 'zBestType', 'zBestSubType', 'zAltProb', 'zAltType', 'zAltSubType', 'zBestPars', 'zAltPars']
    fileDB : Database
    objFieldNames = DataObject.FieldNames()
    validationDB : Database
    fitter: Fitter

    openedSession = Signal(list)
    closedSession = Signal(list)
    xpcaDone = Signal(int)

    def openFiles(self, files, fromFile = False):
        self.closedSession.emit(files)
        path = dirname(files[0])
        self.path = path
        self.fileDB = Database('files', self.fileFieldNames, path)
        self.validationDB = Database('validation', self.objFieldNames, path)
        self.preProcess = Database("preProcess",self.l2FieldNames, path)
        self.fitter = Fitter(path, self.preProcess)          
        
        #get objects from fitter
        self.objects = self.getEmptydataModel(files)

        self.initOptions()
        self.openedSession.emit(files)

    def getEmptydataModel(self,files):
        objs=[]
        for item in list(files):
            #print(item)
            try: #replace with typecheck
                dataModel=getdataModelFromDatabase(item)
                #print(dataModel)
                for name in list(dataModel.keys()):
                    spectra = tool.SDSS_spectrum(self.path / Path(name))
                    objs.append(DataObject.DataObject(name, spectra, dataModel[name]))
            except UnicodeDecodeError:
                obj = self.preProcess.getByName(item)
                spectra = tool.SDSS_spectrum(self.path / Path(item))
                
                if obj is None:
                    dobject = DataObject.DataObject(item, spectra, None)
                else:
                    dobject = DataObject.DataObject(item, spectra, obj)
                objs.append(dobject)
        return objs

    def populate(self):
        #fitter processes files
            for obj in self.objects:
                obj = self.fitter.fitFile(obj,Path(self.path))
                data = self.fileDB.getByName(obj)
                if data is None:
                    self.fileDB.addEntry(obj, self.fileFieldNames, [self.path, obj.category, obj.redshift])     

    def updateCursor(self, delta):
        self.cursor = self.cursor + delta 

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
        if obj.fitting!=None:
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
        try:
            return self.objects[self.cursor]
        except IndexError as e:
            print(self.objects)
            print(self.cursor)
            raise e

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

        self.validationDB.addEntry(object.name, self.catFieldNames, [categorised, category, redshift, note])

    def getDBEntry(self, name):
        row = self.validationDB.getByName(name,None)
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

    def getFileList(self):
        return list(self.fitter.preProcess.df.keys())