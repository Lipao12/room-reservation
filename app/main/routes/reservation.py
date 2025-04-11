from main.routes.websocket import notify_clients
from fastapi import Depends, APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict

# Importação o gerente de conexões
from main.models.settings.db_communication import db_connection_handler

# Criação do APIRouter
router = APIRouter()

# Importação do Repositorio
from main.models.repositories.reservation_repository import ReservationRepository

# Importação dos Controllers
from main.controllers.reservation_creator import ReservationCreator
from main.controllers.reservation_finder import ReservationFinder

# Importação dos necessários para WebSocket
from .websocket import notify_client
import json

def get_reservation_repository():
    conn = db_connection_handler.get_connection()
    return ReservationRepository(conn)

@router.post("/reservations")
async def create_reservation(reservation_data: Dict = Body(), reservation_repository: ReservationRepository = Depends(get_reservation_repository)):
    """
    Cria uma reserva.
    """
    controller = ReservationCreator(reservation_repository)
    response = controller.create(reservation_data)
    if not response['body']:
        raise HTTPException(status_code=404, detail=f"Room with ID {id} not found.")
    
    #await notify_clients(f"Nova reserva criada: {response['body']}")
    #await notify_all("nova_reserva")
    '''await notify_client(json.dumps({
    "type": "reservation_created",
    "data": response["body"]
    }))'''

    return JSONResponse(content=response['body']["reservation_id"], status_code=response['status_code'])

@router.delete("/reservations/{id}")
async def delete_reservation(id: str, reservation_repository: ReservationRepository = Depends(get_reservation_repository)):
    """
    Deleta uma sala específica pelo ID.
    """
    controller = ReservationCreator(reservation_repository)
    response = controller.delete(reservation_id=id)
    if response['status_code'] != 200:
        raise HTTPException(status_code=response['status_code'], detail=response['body'])
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.get("/reservations/{id}")
async def get_reservation_by_id(id: str, reservation_repository: ReservationRepository = Depends(get_reservation_repository)):
    """
    Obtém uma reserva específica pelo ID.

    Retorna um JSON com os dados da sala e o código de status 200.
    """
    controller = ReservationFinder(reservation_repository)
    response = controller.find_by_id(reservation_id=id)
    if not response['body']:
        raise HTTPException(status_code=404, detail=f"Reservation with ID {id} not found.")
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.get("/reservations/user/{id}")
async def get_reservation_by_user(id: str, reservation_repository: ReservationRepository = Depends(get_reservation_repository)):
    """
    Obtém uma reserva por usuário.

    Retorna um JSON com os dados da sala e o código de status 200.
    """
    controller = ReservationFinder(reservation_repository)
    response = controller.find_by_user(user_id=id)
    if not response['body']:
        raise HTTPException(status_code=404, detail=f"No reservation")
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.get("/reservations/room/{id}")
async def get_reservation_by_room(id: str, reservation_repository: ReservationRepository = Depends(get_reservation_repository)):
    """
    Obtém uma reserva por usuário.

    Retorna um JSON com os dados da sala e o código de status 200.
    """
    controller = ReservationFinder(reservation_repository)
    response = controller.find_by_room(room_id=id)
    if not response['body']:
        raise HTTPException(status_code=404, detail=f"No reservation")
    return JSONResponse(content=response['body'], status_code=response['status_code'])