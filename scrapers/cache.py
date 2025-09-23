import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def cache_search(query: str, data: dict, ttl: int = 3600):
    r.setex(f'search:{query}', ttl, json.dumps(data))

def get_cached_search(query: str):
    val = r.get(f'search:{query}')
    return json.loads(val) if val else None
