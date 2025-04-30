import Spec_tools as tool

from json import loads

"""
auxiliary class used by Model to store data for fits-files
"""
class DataObject:

    name: str
    file: tool.SDSS_spectrum
    fitting: dict
    userFitting: dict
    path = str
    category: str
    redshift: float
    validators: set

    def __init__(self, filename, file, fitting = None, path = None, validators = set()):
        self.name = filename
        self.file = file
        self.fitting = fitting
        self.path = path
        if type(validators)==list:
            self.validators=set(validators)
        elif type(validators)!=set:
            raise TypeError("validators is a "+str(type(validators))+", should be a list or set!")
        else:
            self.validators = validators

        if fitting is not None:
            self.category = fitting['zBestSubType']
            self.redshift = fitting['zBest']
        else:
            self.category = None
            self.redshift = None

    def changeRedshift(self, val):
        self.redshift = val

    def changeCategory(self, cat):
        self.category = cat
    
    def getFile(self):
        return self.file
    
#      method not baing used
 #   def toDict(self):
 #       selfDict = {
 #       'path': self.path,
 #       'file' : self.file,
 #       'category' : self.category,
 #       'redshift' : self.redshift}
#
 #       return selfDict
    
#    method not being used
#    def fromDict(dict, fitting):
#        path = dict['path'] 
#        name = path [-21:][:-5]  
#        file = dict['file']
#        category = dict['category']
#        redshift = dict['redshift']
#        
#        object = DataObject(name, file, fitting, path)
#        object.changeCategory(category)
#        object.changeRedshift(redshift)
#
#        return object
#    
#    method not being used
    def fromSeries(series, fitting):
        path = series['path']
        file = series['file']
        category = series['category']
        redshift = series['redshift']

        object = DataObject(path, file, fitting)
        object.changeCategory(category)
        object.changeRedshift(redshift)
        return object