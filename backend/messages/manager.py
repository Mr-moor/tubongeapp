from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

class ConnectionManager:
    def __init__(self):
        self.active = {}  # user_id -> websocket

    async def connect(self, websocket, user_id):
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, websocket):
        for uid, ws in list(self.active.items()):
            if ws == websocket:
                del self.active[uid]

    async def send_to_user(self, user_id, message):
        if user_id in self.active:
            await self.active[user_id].send_text(message)

RATE_LIMIT = 1.0  # seconds

def allowed(self, user_id: int):
    now = time.time()
    last = self.last_message_time.get(user_id, 0)
    if now - last < RATE_LIMIT:
        return False
    self.last_message_time[user_id] = now
    return True
