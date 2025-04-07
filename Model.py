import Spec_tools as tool
from DataObject import DataObject
from fitter import Fitter
from database import Database



class Model:
    cursor = 0
    objects = []
    options: dict
    fileFieldNames = ['name', 'file', 'category', 'redshift']
    fileDB : Database
    catFieldNames = ['name', 'categorized', 'category', 'redshift', 'note']
    categoryDB : Database
    fitter: Fitter

    def __init__(self, path, fromCSV = False):
        
        self.fileDB = Database('files.csv', self.fileFieldNames, path)
        self.categoryDB = Database('data.csv', self.catFieldNames, path)
        self.fitter = Fitter()

        if not fromCSV:
            self.fileDB.populate(self.fitter)
        
        self.objects = self.fileDB.extract(self.fitter)

        # initilaize options
    
    def getState(self):
        return self.objects[self.cursor]
    
    def updateCursor(self, delta):
        self.cursor = self.cursor + delta 

    def setOptions(self, opt, val):
        self.options[opt] = val
    
    def changeRedShift(self, val):
        self.objects[self.cursor].changeRedshift(val)

    def getRedShift(self):
        return float(self.objects[self.cursor].redshift)
    
    def getCategory(self):
        return self.objects[self.cursor].category

    def changeCategory(self, cat):
        self.objects[self.cursor].changeCategory(cat) 

    def addDBEntry(self, categorised, note):
        object = self.objects[self.cursor]

        if categorised:
            category = object.category
            redshift = object.redshift
        else:
            category = None
            redshift = None

        self.categoryDB.addEntry(object.name, categorised, category, redshift, note)

