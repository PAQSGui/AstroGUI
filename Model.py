from fitter import Fitter
from database import Database

"""
Model interfaces between the UI elements and the databases
It also maintains a dictionary of 'options', which are used to change behaviours in the program
Any new options should be added to the dictionary and only accesed with the methods
"""
class Model:
    skygrabNotLoaded = True

    cursor = 0
    objects = []
    options: dict
    path = ""
    fileFieldNames = ['name', 'file', 'category', 'redshift']
    fileDB : Database
    catFieldNames = ['name', 'categorized', 'category', 'redshift', 'note']
    categoryDB : Database
    fitter: Fitter

    def __init__(self, path, fromCSV = False):

        self.path = path
        self.fileDB = Database('files.csv', self.fileFieldNames, path)
        self.categoryDB = Database('data.csv', self.catFieldNames, path)
        self.fitter = Fitter()

        if not fromCSV:
            self.fileDB.populate(self.fitter)
        
        self.objects = self.fileDB.extract(self.fitter)

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

        self.categoryDB.addEntry(object.name, categorised, category, redshift, note)

    def getDBEntry(self, name):
        row = self.categoryDB.getEntry(name)
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
