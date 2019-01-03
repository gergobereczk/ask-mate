import csv


def read_csv(filename):
    with open(filename) as csv_data:
        dict_data = csv.DictReader(csv_data)
        database = []
        for line in dict_data:
            database.append(line)
        return database


def write_csv(from_filename, to_filename, fieldnames, form_data):
    data = read_csv(from_filename)
    data.append(form_data)
    with open(to_filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames)
        for line in data:
            writer.writerow(line)
        return data
