class Database():
    dataFile = ""

    def __init__(self, dataFile):
        self.dataFile = dataFile

    def addEntry(self, name, category, note, redshift):
        with open(self.dataFile, "a") as file:
            if category == "None":
                file.write(name + ", False, None, %s, redshift \n" % note)
            else:
                file.write(name + ", True, %s, None, %f\n" % (category, redshift))

