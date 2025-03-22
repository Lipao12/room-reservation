from fastapi import FastAPI
from ..routes.room import router as room_router
from ..routes.auth import router as auth_router

app = FastAPI()
app.include_router(room_router)
app.include_router(auth_router)
