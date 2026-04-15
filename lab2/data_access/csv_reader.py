import csv
from data_access.interfaces.csv_reader_interface import ICsvReader

class CsvReader(ICsvReader):
    def read_rows(self, file_path):
        rows = []
        with open(file_path, mode='r', encoding='utf-8-sig', newline='') as file:
            sample = file.read(4096)
            file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=";,")
                detected_delimiter = dialect.delimiter
            except csv.Error:
                detected_delimiter = ","
            reader = csv.DictReader(file, delimiter=detected_delimiter)
            
            for row in reader:
                rows.append(row)
                
        return rows
    