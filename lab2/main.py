from data_access.database import Base, engine
from data_access.repository import SqlAlchemyRepository
from data_access.csv_reader import CsvReader
from business.import_service import ImportService, ImportValidationError
from business.import_controller import ImportController
from generator.csv_generator import CsvGenerator


csv_path = "generator/hotels.csv"

def start_csv_generation():
    generator = CsvGenerator(path=csv_path)
    generator.generate()
    print("Successful CSV file generation")

def start_data_import():
    Base.metadata.create_all(bind=engine)

    csv_reader = CsvReader()
    repo = SqlAlchemyRepository()
    service = ImportService(csv_reader=csv_reader, repository=repo)
    controller = ImportController(import_service=service)

    try:
        controller.start_import(csv_path)
        print(f"Successful import from {csv_path}")
    except ImportValidationError as err:
        print(f"Import Validation Error: {err}")
    except Exception as err:
        print(f"Unexpected error: {err}")
    finally:
        repo.close()

if __name__ == '__main__':
    print("Welcome!\n\nAvailable commands:\n" + 
        "1 - Generate CSV\n" +
        "2 - Import data from CSV to database\n" +
        "3 - Exit\n")
    
    while True:
        command = input("Enter: ")
        if command == "1":
            start_csv_generation()
        elif command == "2":
            start_data_import()
        elif command == "3":
            break
        else:
            print("Wrong command.")