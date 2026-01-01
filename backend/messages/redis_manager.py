import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def publish(room, message):
    r.publish(room, json.dumps(message))
