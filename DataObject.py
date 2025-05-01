import Spec_tools as tool

"""
auxiliary class used by Model to store data for fits-files
"""
class DataObject:
    name: str
    file: tool.SDSS_spectrum
    fitting: dict
    path: str
    category: str
    redshift: float

    def __init__(self, filename, file, fitting = None, path = None):
        self.name = filename
        self.file = file
        self.fitting = fitting
        self.path = path

        if fitting is not None:
            self.category = fitting['zBestSubType']
            self.redshift = fitting['zBest']
        else:
            self.category = None
            self.redshift = None

    def changeRedshift(self, value):
        self.redshift = value

    def changeCategory(self, category):
        self.category = category