import csv
from data_access.interfaces.csv_reader_interface import ICsvReader

class CsvReader(ICsvReader):
    def read_rows(self, file_path):
        rows = []
        with open(file_path, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return rows
    