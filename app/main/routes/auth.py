from fastapi import Depends, APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict

# Importação o gerente de conexões
from main.models.settings.db_communication import db_connection_handler

# Criação do APIRouter
router = APIRouter()

# Importação do Repositorio
from main.models.repositories.user_repository import UserRepository

# Importação dos Controllers
from main.controllers.auth_controller import UserAuthController

def get_user_repository():
    conn = db_connection_handler.get_connection()
    return UserRepository(conn)

@router.post("/login")
async def login(user_data: Dict = Body(), user_repository: UserRepository = Depends(get_user_repository)):
    """
    Faz o login.

    Retorna um JSON com o token e o tipo e o código de status 200.
    """
    controller = UserAuthController(user_repository)
    response = controller.login(email=user_data['email'], password=user_data['password'])
    if not response['body']:
        raise HTTPException(status_code=404, detail=f"Room with ID {id} not found.")
    
    return JSONResponse(content=response['body'], status_code=response['status_code'])

@router.post("/register")
async def register(user_data: Dict = Body(), user_repository: UserRepository = Depends(get_user_repository)):
    """
    Faz o Registro.

    Retorna o nome e o código de status 200.
    """
    controller = UserAuthController(user_repository)
    response = controller.register(user_data)

    if not response['body']:
        raise HTTPException(status_code=404, detail=f"Room with ID {id} not found.")
    
    return JSONResponse(content=response['body'], status_code=response['status_code'])
