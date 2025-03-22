from fastapi import FastAPI
from ..routes.room import router as room_router

app = FastAPI()
app.include_router(room_router)
