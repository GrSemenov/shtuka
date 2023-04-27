import csv

class FilesWriter():
    def write_csv(self, dots):
        myFile = open('dots.csv', 'w')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(dots)
