from abc import ABC, abstractmethod

class ICsvReader(ABC):
    @abstractmethod
    def read_rows(self, file_path: str):
        pass