import json
import sys
from strategies import ConsoleOutputStrategy, RedisOutputStrategy, KafkaOutputStrategy
from data_reader import CSVReader
from data_processor import DataProcessor

def load_config(config_path: str = 'config.json') -> dict:
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Critical error: config file {config_path} not found.")
        sys.exit(1)

def main():
    config = load_config()
    active_strategy_name = config.get('active_strategy', 'console')
    dataset_path = config.get('dataset_path', 'hotels.csv')

    if active_strategy_name == 'redis':
        selected_strategy = RedisOutputStrategy(config['redis'])
    elif active_strategy_name == 'kafka':
        selected_strategy = KafkaOutputStrategy(config['kafka'])
    else:
        selected_strategy = ConsoleOutputStrategy()
    
    processor = DataProcessor(selected_strategy)
    reader = CSVReader(dataset_path, delimiter=";")

    print("=" * 40)
    print(f"Start information processing...")
    print(f"Dataset: {dataset_path}")
    print(f"Active strategy: {active_strategy_name.upper()}")
    print("=" * 40)
    
    count = 0
    for data_row in reader.read_data():
        processor.process_row(data_row)
        count += 1

    print("=" * 40)
    print(f"Data processing complete. Rows processed: {count}")

if __name__ == "__main__":
    main()