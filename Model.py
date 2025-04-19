from fitter import Fitter
from database_json import Database
from os.path import dirname
import DataObject

class Model:
    skygrabNotLoaded = True

    cursor = 0
    objects = []
    options: dict
    fileFieldNames = ['name', 'file', 'category', 'redshift']
    fileDB : Database
    objFieldNames = DataObject.FieldNames()
    validationDB : Database
    fitter: Fitter
    #OPTION Params
    lineThickness = 0.5
    redshiftRez = 1e4
    redshiftMax = 6
    redshiftMin = 0

    def __init__(self, files, fromFile = False):
        path = dirname(files[0])
        self.path = path
        self.fileDB = Database('files', self.fileFieldNames, path)
        self.validationDB = Database('validation', self.objFieldNames, path)
        self.fitter = Fitter(path)

        #fitter processes files
        if not fromFile:
            self.fitter.populate(files,path)
            for file in files:
                data = self.fileDB.getByName(file)
                if data == []:
                        self.fileDB.addEntry(file, self.fileFieldNames, [path, None, None])
                
        
        #get objects from fitter
        self.objects = self.fitter.getModel()

        self.initOptions()

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
        return float(self.objects[self.cursor].redshift)
    
    def getCategory(self):
        return self.objects[self.cursor].category
    
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
            }
        self.options = options

    def resetYLimit(self):
        self.options['yLimit'] = False
        self.options['ymin'] = 0
        self.options['ymax'] = 0

    def getFileList(self):
        return list(self.fitter.preProcess.model.keys())