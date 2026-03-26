from datetime import datetime
from business.interfaces.import_service_interface import IImportService

from data_access.interfaces.repository_interface import IRepository
from data_access.interfaces.csv_reader_interface import ICsvReader

class ImportServiceError(Exception):
    pass
class ImportValidationError(ImportServiceError):
    pass

class ImportService(IImportService):
    REQUIRED_FIELDS = [
        "chain_name",
        "hotel_name",
        "description",
        "email",
        "country",
        "city",
        "street",
        "number",
        "room_type",
        "capacity",
        "price",
        "room_number",
        "checkin",
        "checkout",
        "status",
        "rating",
        "comment",
        "review_date"
    ]
    
    def __init__(self, repository:IRepository, csv_reader:ICsvReader):
        self.csv_reader = csv_reader
        self.repository = repository
    
    def import_from_csv(self, file_path:str):
        rows = self.csv_reader.read_rows(file_path)

        try:
            for index, row in enumerate(rows, start=2):
                self._validate_row(row, index)

                chain = self.repository.get_or_create_hotel_chain(name=row["chain_name"].strip())

                location = self.repository.get_or_create_location(
                    country=row["country"].strip(),
                    city=row["city"].strip(),
                    street=row["street"].strip(),
                    number=row["number"].strip(),
                )

                hotel = self.repository.get_or_create_hotel(
                    name=row["hotel_name"].strip(),
                    description=row["description"].strip(),
                    contact_email=row["email"].strip(),
                    hotel_chain=chain,
                    location=location
                )

                room_type = self.repository.get_or_create_room_type(
                    name=row["room_type"].strip(),
                    capacity=self._parse_positive_int(row["capacity"], "capacity", index),
                    base_price=self._parse_price(row["price"], "price", index),
                    hotel=hotel
                )

                room = self.repository.get_or_create_room(
                    room_number=row["room_number"].strip(),
                    is_available=True,
                    room_type=room_type
                )
                
                reservation = self.repository.get_or_create_reservation(
                    check_in_date=datetime.fromisoformat(row["checkin"]),
                    check_out_date=datetime.fromisoformat(row["checkout"]),
                    status=row["status"],
                    room=room
                )

                review = self.repository.get_or_create_review(
                    comment=row["comment"],
                    date_posted=datetime.fromisoformat(row["review_date"]),
                    rating=row["rating"],
                    hotel=hotel,
                )
            
            self.repository.commit()
        except Exception:
            self.repository.rollback()
            raise

    def _validate_row(self, row:dict, row_number:int):
        for field in self.REQUIRED_FIELDS:
            if field not in row or not str(row[field]).strip():
                raise ImportValidationError(
                    f"Row {row_number}: field '{field} is required'"
                )
    
    def _parse_positive_int(self, value: str, field_name: str, row_number: int) -> int:
        try:
            parsed = int(value)
        except ValueError:
            raise ImportValidationError(f"{field_name} must be int")

        if parsed <= 0:
            raise ImportValidationError(f"{field_name} must be > 0")

        return parsed


    def _parse_price(self, value: str, field_name: str, row_number: int) -> float:
        try:
            return float(value)
        except ValueError:
            raise ImportValidationError(f"{field_name} must be decimal")