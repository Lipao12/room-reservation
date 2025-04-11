from fastapi import FastAPI,WebSocket
from ..routes.room import router as room_router
from ..routes.auth import router as auth_router
from ..routes.reservation import router as reservation_router
from ..routes.websocket import router as ws_router
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(room_router)
app.include_router(auth_router)
app.include_router(reservation_router)
app.include_router(ws_router)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <button onclick="connect()">Conectar</button>
        <button onclick="sendReservationRequest()">Enviar Pedido de Reserva</button>
        <p id="status">Status: Desconectado</p>
        <p id="response">Resposta: Nenhuma</p>

        <script>
            let ws;

            function connect() {
                ws = new WebSocket("ws://localhost:8000/ws");
                document.getElementById("status").innerText = "Status: Conectando...";

                ws.onopen = function() {
                    document.getElementById("status").innerText = "Status: Conectado!";
                };

                ws.onmessage = function(event) {
                    document.getElementById("response").innerText = "Resposta: " + event.data;
                };

                ws.onclose = function() {
                    document.getElementById("status").innerText = "Status: Desconectado";
                };
            }

            function sendReservationRequest() {
                const roomId = prompt("Digite o ID da sala que você deseja buscar:");
                if (roomId) {
                    ws.send(`room_id:${roomId}`);
                } else {
                    alert("Por favor, insira um ID da Sala.");
                }
            }
        </script>
    </body>
</html>

"""

@app.get("/")
async def get():
    return HTMLResponse(html)