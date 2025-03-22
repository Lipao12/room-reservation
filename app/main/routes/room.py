from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

# Importação o gerente de conexões
from main.models.settings.db_communication import db_connection_handler

# Criação do APIRouter
router = APIRouter()

# Importação do Repositorio
from main.models.repositories.room_repository import RoomRepository

# Importação dos Controllers
from main.controllers.room_creator import RoomCreator
from main.controllers.room_finder import RoomFinder 
print("dfhj")
def get_room_repository():
    conn = db_connection_handler.get_connection()
    return RoomRepository(conn)

@router.get("/hi/{who}")
def hello(who):
    return f"Hello? {who}?"

@router.get("/rooms")
def get_rooms(room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomFinder(room_repository)
    response = controller.find_all()
    return JSONResponse(response['body']), response['status_code']

@router.get("/rooms/{id}")
def get_rooms(room_id: str, room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomFinder(room_repository)
    response = controller.find_one(room_id=room_id)
    return JSONResponse(response['body']), response['status_code']

@router.post("/rooms")
def create_room(room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomCreator(room_repository)
    response = controller.create()
    return JSONResponse(response['body']), response['status_code']

@router.delete("/rooms/{id}")
def delete_rooms(room_id: str, room_repository: RoomRepository = Depends(get_room_repository)):
    controller = RoomCreator(room_repository)
    response = controller.delete(room_id=room_id)
    return JSONResponse(response['body']), response['status_code']