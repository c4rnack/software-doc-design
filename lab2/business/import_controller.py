from business.interfaces.controller_interface import IController
from business.interfaces.import_service_interface import IImportService

class ImportController(IController):
    def __init__(self, import_service:IImportService):
        self.import_service = import_service
    
    def start_import(self, file_path:str):
        self.import_service.import_from_csv(file_path)