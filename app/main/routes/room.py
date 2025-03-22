from fastapi import Depends
from fastapi.responses import JSONResponse

from ..server.server import app

# Importação o gerente de conexões
from app.main.models.settings.db_communication import db_connection_handler

# Importação do Repositorio
from app.main.models.repositories.room_repository import RoomRepository

# Importação dos Controllers
from app.main.controllers.room_creator import RoomCreator
from app.main.controllers.room_finder import RoomFinder 

def get_room_repository():
    conn = db_connection_handler.get_connection()
    return RoomRepository(conn)

@app.get("/hi/{who}")
def hello(who):
    return f"Hello? {who}?"

@app.get("/rooms")
def get_rooms(room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomFinder(room_repository)
    response = controller.find_all()
    return JSONResponse(response['body']), response['status_code']

@app.get("/rooms/{id}")
def get_rooms(room_id: str, room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomFinder(room_repository)
    response = controller.find_one(room_id=room_id)
    return JSONResponse(response['body']), response['status_code']

@app.post("/rooms")
def create_room(room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomCreator(room_repository)
    response = controller.create()
    return JSONResponse(response['body']), response['status_code']

@app.delete("/rooms/{id}")
def delete_rooms(room_id: str, room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomCreator(room_repository)
    response = controller.delete(room_id=room_id)
    return JSONResponse(response['body']), response['status_code']