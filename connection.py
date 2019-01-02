import csv


def read_csv(filename):
    with open(filename) as csv_data:
        dict_data = csv.DictReader(csv_data)
        database = []
        print (dict_data)
        for line in dict_data:
            database.append(line)
        return database
