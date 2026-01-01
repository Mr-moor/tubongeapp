pubsub = r.pubsub()
pubsub.subscribe("chat")

for msg in pubsub.listen():
    broadcast(msg["data"])
