from fastapi import WebSocket, WebSocketDisconnect
from backend.messages.manager import ConnectionManager

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# backend/messages/websocket.py
from backend.notifications.push import send_push

await manager.send_room(room_id, data)
# Send push to offline users
for user_id in offline_users:
    send_push(user_push_token[user_id], "New Message", "You have a new message")

elif data["type"] == "read":
    msg_id = data["message_id"]
    msg = db.query(Message).get(msg_id)
    msg.delivered = True
    db.commit()
    await manager.send_room(room_id, {"type": "read", "message_id": msg_id})
def get_current_user_ws(token: str):
    # decode JWT
    return user
