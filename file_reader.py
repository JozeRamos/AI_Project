import csv
from establishment import Establishment


class FileReader:

    def transform_to_list(str):
        return str
        

    @staticmethod
    def get_establishments():
        establishment_list = []
        with open('establishments.csv', mode='r') as file:

            csv_file = csv.reader(file)
            first = True
            for lines in csv_file:
                if first:
                    first = False
                    continue

                establishment_list.append(
                    Establishment(int(lines[0]), lines[1], lines[2], lines[3], lines[4], float(lines[5]), float(lines[6]),
                                                float(lines[7]), int(lines[8]), eval(lines[9])))
        return establishment_list

    @staticmethod
    def get_distances():
        distances_matrix = []
        with open('distances.csv', mode='r') as file:
            # reading the CSV file
            csv_file = csv.reader(file)
            first = True
            # displaying the contents of the CSV file
            for lines in csv_file:
                if first:
                    first = False
                    continue
                distances_matrix.append(lines[1:])
        return distances_matrix

