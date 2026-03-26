from data_access.interfaces.repository_interface import IRepository
from data_access.database import SessionLocal
from data_access.models import (
    HotelChain,
    Location,
    Hotel,
    RoomType, 
    Room, 
    Review,
    Reservation,
)

class SqlAlchemyRepository(IRepository):
    def __init__(self):
        self.session = SessionLocal()
    
    def get_or_create_hotel_chain(self, name):
        hotel_chain = self.session.query(HotelChain).filter_by(name=name).first()
        if hotel_chain:
            return hotel_chain
        
        hotel_chain = HotelChain(name=name)
        self.session.add(hotel_chain)
        self.session.flush()
        return hotel_chain
    
    def get_or_create_location(self, country, city, street, number):
        location = self.session.query(Location).filter_by(country=country, city=city, street=street, number=number).first()
        if location:
            return location
        
        location = Location(country=country, city=city, street=street, number=number)
        self.session.add(location)
        self.session.flush()
        return location
    
    def get_or_create_hotel(self, name, description, contact_email, hotel_chain, location):
        hotel = self.session.query(Hotel).filter_by(name=name, hotelChainId=hotel_chain.hotelChainId).first()
        if hotel:
            return hotel
        
        hotel = Hotel(name=name, description=description, contactEmail=contact_email, location=location, hotel_chain=hotel_chain)
        self.session.add(hotel)
        self.session.flush()
        return hotel

    def get_or_create_room_type(self, name, capacity, base_price, hotel):
        room_type = self.session.query(RoomType).filter_by(name=name, capacity=capacity, hotelId=hotel.hotelId).first()
        if room_type:
            return room_type
        
        room_type = RoomType(name=name, capacity=capacity, basePrice=base_price, hotel=hotel)
        self.session.add(room_type)
        self.session.flush()
        return room_type
    
    def get_or_create_room(self, room_number, is_available, room_type):
        room = self.session.query(Room).filter_by(roomNumber=room_number, roomTypeId=room_type.roomTypeId).first()
        if room:
            return room
        
        room = Room(roomNumber=room_number, isAvailable=is_available, room_type=room_type)
        self.session.add(room)
        self.session.flush()
        return room
    
    def get_or_create_review(self, comment, rating, date_posted, hotel):
        review = self.session.query(Review).filter_by(comment=comment, rating=rating, hotelId = hotel.hotelId).first()
        if review:
            return review
        
        review = Review(comment=comment, rating=rating, datePosted=date_posted, hotel=hotel)
        self.session.add(review)
        self.session.flush()
        return review
    
    def get_or_create_reservation(self, check_in_date, check_out_date, status, room):
        reservation = self.session.query(Reservation).filter_by(checkInDate=check_in_date, checkOutDate=check_out_date, roomId=room.roomId).first()
        if reservation:
            return reservation
        
        reservation = Reservation(checkInDate=check_in_date, checkOutDate=check_out_date, status=status, room=room)
        self.session.add(reservation)
        self.session.flush()
        return reservation
    
    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()