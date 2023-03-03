import csv
from establishment import Establishment


class FileReader:

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
                    Establishment(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6],
                                                lines[7], lines[8], lines[9]))
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
