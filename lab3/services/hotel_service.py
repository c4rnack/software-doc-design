from sqlalchemy.orm import Session
from data_access.models import Hotel, Location

class HotelService:
    @staticmethod
    def get_all_hotels(db: Session):
        return db.query(Hotel).all()

    @staticmethod
    def get_hotel(db: Session, hotel_id: int):
        return db.query(Hotel).filter(Hotel.hotelId == hotel_id).first()

    @staticmethod
    def create_hotel(db: Session, name: str, description: str, contactEmail: str, country: str, city: str, street: str, number: str):

        new_location = Location(country=country, city=city, street=street, number=number)
        db.add(new_location)
        db.commit()
        db.refresh(new_location)

        new_hotel = Hotel(
            name=name, 
            description=description, 
            contactEmail=contactEmail, 
            locationId=new_location.locationId
        )
        db.add(new_hotel)
        db.commit()
        db.refresh(new_hotel)
        return new_hotel

    @staticmethod
    def update_hotel(db: Session, hotel_id: int, name: str, description: str, contactEmail: str, country: str, city: str, street: str, number: str):
        db_hotel = db.query(Hotel).filter(Hotel.hotelId == hotel_id).first()
        if db_hotel:
            db_hotel.name = name
            db_hotel.description = description
            db_hotel.contactEmail = contactEmail

            if db_hotel.location:
                db_hotel.location.country = country
                db_hotel.location.city = city
                db_hotel.location.street = street
                db_hotel.location.number = number
                
            db.commit()
            db.refresh(db_hotel)
        return db_hotel

    @staticmethod
    def delete_hotel(db: Session, hotel_id: int):
        db_hotel = db.query(Hotel).filter(Hotel.hotelId == hotel_id).first()
        if db_hotel:
            loc_to_delete = db_hotel.location
            db.delete(db_hotel)
            if loc_to_delete:
                db.delete(loc_to_delete)
            db.commit()
        return db_hotel