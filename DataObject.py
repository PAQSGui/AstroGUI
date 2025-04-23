import Spec_tools as tool

class DataObject:

    name: str
    file: tool.SDSS_spectrum
    fitting: dict
    category: str
    redshift: float

    def __init__(self, filename, file, fitting):
        self.name = filename
        self.file = file
        self.fitting = fitting
        try:
            self.category = fitting['zBestSubType']
            self.redshift = fitting['zBest']
        except:
            self.category = None
            self.redshift = 0

    def changeRedshift(self, val):
        self.redshift = val

    def changeCategory(self, cat):
        self.category = cat
    
    def getFile(self):
        return self.file

    def toDict(self):
        selfDict = {
        'name': self.name,
        'file' : self.file,
        'category' : self.category,
        'redshift' : self.redshift}

        return selfDict
    
    def fromDict(dict, fitting):
        name = dict['name']
        file = dict['file']
        category = dict['category']
        redshift = dict['redshift']

        object = DataObject(name, file, fitting)
        object.changeCategory(category)
        object.changeRedshift(redshift)

        return object
    
    
    def fromSeries(name, series, fitting):
        file = series["file"]
        category = series["category"]
        redshift = series["redshift"]

        object = DataObject(name, file, fitting)
        object.changeCategory(category)
        object.changeRedshift(redshift)
        return object