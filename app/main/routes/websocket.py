from typing import Dict, List
from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
import httpx

# Criação do APIRouter
router = APIRouter()

active_connections: List[WebSocket] = []

'''@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Conexão WebSocket estabelecida!")

    while True:
        data = await websocket.receive_text()

        if data.startswith("room_id:"):
            room_id = data.split(":")[1]
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://localhost:8000/reservations/room/{room_id}")
                    if response.status_code == 200:
                        await websocket.send_text(response.text)
                    else:
                        await websocket.send_text(f"Erro: {response.text}")
            except Exception as e:
                await websocket.send_text(f"Erro: {str(e)}")
        else:
            await websocket.send_text(f"Mensagem recebida: {data}")
'''

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    await websocket.send_text("Conexão WebSocket estabelecida!")

    try:
        while True:
            data = await websocket.receive_text()

            if data.startswith("room_id:"):
                room_id = data.split(":")[1]
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"http://localhost:8000/reservations/room/{room_id}")
                        if response.status_code == 200:
                            await websocket.send_text(response.text)
                        else:
                            await websocket.send_text(f"Erro: {response.text}")
                except Exception as e:
                    await websocket.send_text(f"Erro: {str(e)}")
            else:
                await websocket.send_text(f"Mensagem recebida: {data}")
    finally:
        active_connections.remove(websocket)  # Remove a conexão quando o cliente desconectar

# Função para notificar todos os clientes conectados
async def notify_clients(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@router.get("/ws/health")
async def ws_health_check():
    return JSONResponse(content={"message": "WS service is running"}, status_code=200)

@router.get("/ws/status")
async def ws_status():
    return JSONResponse(content={"status": "Active"}, status_code=200)

