import csv

def read_csv(filename):
    database = []
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            database.append(line)
    del database[0]
    return database
