from strategies import OutputStrategy

class DataProcessor:
    def __init__(self, strategy: OutputStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: OutputStrategy):
        """Allow to change strategy while programm execution"""
        self._strategy = strategy

    def process_row(self, row: dict):
        """
        Additional logic can be added here
        """
        if not row:
            return
            
        self._strategy.write(row)