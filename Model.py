from fitter import Fitter
from database import Database

class Model:
    cursor = 0
    objects = []
    options: dict
    path = ""
    fileFieldNames = ['name', 'file', 'category', 'redshift']
    fileDB : Database
    catFieldNames = ['name', 'categorized', 'category', 'redshift', 'note']
    categoryDB : Database
    fitter: Fitter
    #OPTION Params
    lineThickness = 0.5
    redshiftRez = 1e4
    redshiftMax = 6
    redshiftMin = 0

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
        print(val)
    
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


