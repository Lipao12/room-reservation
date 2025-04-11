from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
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
connected_clients: List[WebSocket] = []

async def notify_all(message: str):
    for ws in connected_clients:
        try:
            await ws.send_text(message)
        except Exception:
            connected_clients.remove(ws)

async def notify_client(websocket: WebSocket, message: str):
    try:
        await websocket.send_text(message)
    except Exception as e:
        print(f"Erro ao notificar cliente: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)

@router.websocket("/ws/rooms")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # opcional: pode ignorar se for só para enviar
    except Exception as e:
        print(f"WebSocket desconectado: {e}")
    finally:
        connected_clients.remove(websocket)

client_sockets: Dict[str, WebSocket] = {} 
@router.websocket("/ws/reservations")
async def reservation_updates(websocket: WebSocket, user_id: str):
    await websocket.accept()
    client_sockets[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # Mantém conexão aberta
    except WebSocketDisconnect:
        del client_sockets[user_id]


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

