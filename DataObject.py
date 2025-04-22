import Spec_tools as tool

def FieldNames():
    return ['name', 'categorized', 'params', 'validated', 'validators',  'note']

"""
auxiliary class used by Model to store data for fits-files
"""
class DataObject:

    name: str
    file: tool.SDSS_spectrum
    fitting: dict
    userFitting: dict
    category: str
    redshift: float

    def __init__(self, filename, file, fitting = None):
        self.name = filename
        self.file = file
        self.fitting = fitting
        if fitting!=None:
            self.category = fitting['zBestSubType']
            self.redshift = fitting['zBest']

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