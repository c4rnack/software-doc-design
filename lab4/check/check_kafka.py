import json
from confluent_kafka import Consumer

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['kafka']

consumer = Consumer({
    'bootstrap.servers': config['bootstrap_servers'],
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([config['topic']])

print(f"Waiting for a message from topic '{config['topic']}' (Ctrl+C to stop)...")

try:
    messages_read = 0
    while messages_read < 5:
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        print(f"Received: {msg.value().decode('utf-8')}")
        messages_read += 1
        
except KeyboardInterrupt:
    pass
finally:
    consumer.close()