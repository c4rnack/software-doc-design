import json
from redis import Redis

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['redis']

client = Redis(
    host=config['host'], 
    port=config['port'], 
    password=config['password'], 
    ssl=True, 
    decode_responses=True
)

keys = client.keys('hotel:*')
print(f"Redis: {len(keys)}")

if keys:
    print(f"\nData example for key:{keys[0]}:")
    print(client.get(keys[0]))