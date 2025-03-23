from fastapi import Depends, APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict

# Importação o gerente de conexões
from main.models.settings.db_communication import db_connection_handler

# Criação do APIRouter
router = APIRouter()

# Importação do Repositorio
from main.models.repositories.room_repository import RoomRepository

# Importação dos Controllers
from main.controllers.room_creator import RoomCreator
from main.controllers.room_finder import RoomFinder 

def get_room_repository():
    conn = db_connection_handler.get_connection()
    return RoomRepository(conn)

@router.get("/rooms")
async def get_rooms(room_repository: RoomRepository = Depends(get_room_repository)):
    """
    Obtém todas as salas cadastradas.

    Retorna um JSON com a lista de salas e o código de status 200.
    """
    controller = RoomFinder(room_repository)
    response = controller.find_all()
    if not response['body']:
        raise HTTPException(status_code=404, detail="No rooms found.")
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.get("/rooms/{id}")
async def get_room_by_id(id: str, room_repository: RoomRepository = Depends(get_room_repository)):
    """
    Obtém uma sala específica pelo ID.

    Retorna um JSON com os dados da sala e o código de status 200.
    """
    controller = RoomFinder(room_repository)
    response = controller.find_one(room_id=id)
    if not response['body']:
        raise HTTPException(status_code=404, detail=f"Room with ID {id} not found.")
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.post("/rooms")
async def create_room(room_info: Dict = Body(), room_repository: RoomRepository = Depends(get_room_repository)):
    """
    Cria uma nova sala.
    
    - **name**: Nome da sala
    - **capacity**: Capacidade da sala
    
    Exemplo de corpo da requisição:
    ```json
    {
      "name": "Sala 3",
      "capacity": 15
    }
    ```
    """
    controller = RoomCreator(room_repository)
    response = controller.create(room_info)
    if response['status_code'] != 201:
        raise HTTPException(status_code=response['status_code'], detail=response['body'])
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.delete("/rooms/{id}")
async def delete_rooms(id: str, room_repository: RoomRepository = Depends(get_room_repository)):
    """
    Deleta uma sala específica pelo ID.
    """
    controller = RoomCreator(room_repository)
    response = controller.delete(room_id=id)
    if response['status_code'] != 200:
        raise HTTPException(status_code=response['status_code'], detail=response['body'])
    return JSONResponse(content=response['body'], status_code=response['status_code'])
