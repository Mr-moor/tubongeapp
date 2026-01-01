from fastapi import WebSocket
from backend.auth.jwt import decode_token

async def authenticate_websocket(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return None

    payload = decode_token(token)
    return payload  # contains user_id, role
