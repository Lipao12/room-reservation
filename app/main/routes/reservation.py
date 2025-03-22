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
    
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.delete("/reservations/{id}")
async def delete_rooms(id: str, reservation_repository: ReservationRepository = Depends(get_reservation_repository)):
    """
    Deleta uma sala específica pelo ID.
    """
    controller = ReservationCreator(reservation_repository)
    response = controller.delete(reservation_id=id)
    if response['status_code'] != 200:
        raise HTTPException(status_code=response['status_code'], detail=response['body'])
    return JSONResponse(content=response['body'], status_code=response['status_code'])

