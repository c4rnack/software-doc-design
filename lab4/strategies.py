import json
from redis import Redis
from abc import ABC, abstractmethod
from confluent_kafka import Producer

class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data: dict):
        pass

class ConsoleOutputStrategy(OutputStrategy):
    def write(self, data: dict):
        print(f"[CONSOLE] Saved: hotel '{data['hotel_name']}' in city {data['city']} (ID: {data['id']})")

class RedisOutputStrategy(OutputStrategy):
    def __init__(self, config: dict):
        self.client = Redis(
            host=config['host'],
            port=config['port'],
            password=config['password'],
            ssl=True,
            decode_responses=True
        )

    def write(self, data: dict):
        redis_key = f"hotel:{data['id']}"
        self.client.set(redis_key, json.dumps(data))
        print(f"[REDIS] Data saved with key: {redis_key}")

class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, config: dict):
        conf = {'bootstrap.servers': config['bootstrap_servers']}
        self.producer = Producer(conf)
        self.topic = config['topic']

    def write(self, data: dict):
        self.producer.produce(self.topic, value=json.dumps(data))
        self.producer.flush()
        print(f"[KAFKA] Data for ID {data['id']} sent to topic '{self.topic}'")