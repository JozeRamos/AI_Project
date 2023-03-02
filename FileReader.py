import csv
import Establishment

class FileReader:
    
    @staticmethod
    def getEstablishments():
        # opening the CSV file
        est = []
        with open('establishments.csv', mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)

            # displaying the contents of the CSV file
            first = True
            for lines in csvFile:
                if(first):
                    first = False 
                    continue
                est.append(Establishment.Establishment(lines[0],lines[1],lines[2],lines[3],lines[4],lines[5],lines[6],lines[7],lines[8],lines[9]))
        return est


    @staticmethod
    def getDistances():
        with open('distances.csv', mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)

            # displaying the contents of the CSV file
            for lines in csvFile:
                print(lines)
