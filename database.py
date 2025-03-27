import csv

## Saves the follwing fields in a csv file:
#  name, boolean indicating wheter the object has been categorized, category if applicable else none, notes, redshift if applicable else 0

#  should also save:
# the date

class Database():
    dataFile = ""
    fieldNames = ""

    def __init__(self, dataFile, fieldNames = []):
        self.dataFile = dataFile
        self.fieldNames = fieldNames
        if fieldNames != []:
            with open(self.dataFile, 'a', newline='') as file:
                writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
                writer.writeheader()            

    def addEntry(self, name, category, note, redshift):
        with open(self.dataFile, 'a', newline='') as file:
            writer = csv.writer(file)
            if category == "None":
                writer.writerow([name, False, None, note, redshift])
            else:
                writer.writerow([name, True, category, None, redshift]) # ", True, %s, None, %f\n" % (category, redshift))

    def addFitting(self, l2):
        with open(self.dataFile, 'a', newline='') as file:
            writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
            writer.writerow(l2)

    def getFitting(self, name):
        with open(self.dataFile, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[self.fieldNames[0]] == name:
                    return row
            return []

