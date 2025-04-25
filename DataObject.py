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

    def __init__(self, filename, file, fitting = None, path = None):
        self.name = filename
        self.file = file
        self.fitting = fitting
        self.path=path
        try:
            if fitting is not None:
                self.category = fitting['zBestSubType']
                self.redshift = fitting['zBest']
        except Exception as e:
            print(type(fitting))
            print(fitting)
            raise e

    def changeRedshift(self, val):
        self.redshift = val

    def changeCategory(self, cat):
        self.category = cat
    
    def getFile(self):
        return self.file

    def toDict(self):
        selfDict = {
        'name': self.path,
        'file' : self.file,
        'category' : self.category,
        'redshift' : self.redshift}

        
        return selfDict
    
    def fromDict(dict, fitting):
        path = dict['name']
        name = path[-21:][:-5]  
        file = dict['file']
        category = dict['category']
        redshift = dict['redshift']
        
        object = DataObject(name, file, fitting,path)
        object.changeCategory(category)
        object.changeRedshift(redshift)

        return object
    
    
    def fromSeries(series, fitting):
        name = series['name']
        file = series['file']
        category = series['category']
        redshift = series['redshift']

        object = DataObject(name, file, fitting)
        object.changeCategory(category)
        object.changeRedshift(redshift)
        return object