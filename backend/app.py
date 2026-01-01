from fastapi import FastAPI
from backend.auth.router import router as auth_router
from backend.users.router import router as users_router
from backend.content.router import router as content_router
from backend.messages.websocket import ws_router

app = FastAPI(title="Tubonge API")

app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(content_router, prefix="/content")
app.include_router(ws_router, prefix="/ws")
