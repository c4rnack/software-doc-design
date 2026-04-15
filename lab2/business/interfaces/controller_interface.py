from abc import ABC, abstractmethod

class IController(ABC):
    @abstractmethod
    def start_import(self, file_path):
        pass