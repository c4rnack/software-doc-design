from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, Date
from sqlalchemy.orm import relationship

from .database import Base

class HotelChain(Base):
    __tablename__ = 'hotel_chain'

    hotelChainId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    # One-to-Many relationship with Hotel
    hotels = relationship("Hotel", back_populates="hotel_chain", cascade="all, delete-orphan")

class Location(Base):
    __tablename__ = 'location'

    locationId = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    street = Column(String(100), nullable=False)
    number = Column(String(100), nullable=False)

    # One-to-One relationship with Hotel
    hotel = relationship("Hotel", back_populates="location", uselist=False)

class Hotel(Base):
    __tablename__ = 'hotel'

    hotelId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    contactEmail = Column(String(255))

    # Foreign Keys
    hotelChainId = Column(Integer, ForeignKey('hotel_chain.hotelChainId'))
    locationId = Column(Integer, ForeignKey('location.locationId'), unique=True) # unique=True enforces 1-to-1

    # Relationships
    hotel_chain = relationship("HotelChain", back_populates="hotels")
    location = relationship("Location", back_populates="hotel")
    room_types = relationship("RoomType", back_populates="hotel", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="hotel", cascade="all, delete-orphan")

class RoomType(Base):
    __tablename__ = 'room_type'

    roomTypeId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    basePrice = Column(Numeric(10, 2), nullable=False)

    # Foreign Key
    hotelId = Column(Integer, ForeignKey('hotel.hotelId'))

    # Relationships
    hotel = relationship("Hotel", back_populates="room_types")
    rooms = relationship("Room", back_populates="room_type", cascade="all, delete-orphan")

class Room(Base):
    __tablename__ = 'room'

    roomId = Column(Integer, primary_key=True, autoincrement=True)
    roomNumber = Column(String(100), nullable=False)
    isAvailable = Column(Boolean, default=True, nullable=False)

    # Foreign Key
    roomTypeId = Column(Integer, ForeignKey('room_type.roomTypeId'))

    # Relationships
    room_type = relationship("RoomType", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = 'review'

    reviewId = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(String(255))
    rating = Column(Integer, nullable=False)
    datePosted = Column(Date, nullable=False)

    # Foreign Key
    hotelId = Column(Integer, ForeignKey('hotel.hotelId'))

    # Relationships
    hotel = relationship("Hotel", back_populates="reviews")

class Reservation(Base):
    __tablename__ = 'reservation'

    reservationId = Column(Integer, primary_key=True, autoincrement=True)
    checkInDate = Column(Date, nullable=False)
    checkOutDate = Column(Date, nullable=False)
    status = Column(String(255), nullable=False)

    # Foreign Key
    roomId = Column(Integer, ForeignKey('room.roomId'))

    # Relationships
    room = relationship("Room", back_populates="reservations")