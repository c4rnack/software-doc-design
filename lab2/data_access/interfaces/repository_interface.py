from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def get_or_create_hotel_chain(self, name:str):
        pass

    @abstractmethod
    def get_or_create_location(self, country:str, city:str, street:str, number:str):
        pass

    @abstractmethod
    def get_or_create_hotel(self, name:str, description:str, contact_email:str, hotel_chain, location):
        pass

    @abstractmethod
    def get_or_create_room_type(self, name:str, capacity:int, base_price:int, hotel):
        pass

    @abstractmethod
    def get_or_create_room(self, room_number:str, is_available:bool, room_type):
        pass

    @abstractmethod
    def get_or_create_review(self, comment:str, rating:int, date_posted, hotel):
        pass

    @abstractmethod
    def get_or_create_reservation(self, check_in_date, check_out_date, status:str, room):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close(self):
        pass