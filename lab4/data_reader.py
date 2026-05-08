import csv

class CSVReader:
    def __init__(self, file_path: str, delimiter: str = ";"):
        self.file_path = file_path
        self.delimiter = delimiter

    def read_data(self):
        """Read CSV file and return rows"""
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=self.delimiter)
                for row in reader:
                    yield row
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found!")
            return []