from ..server.server import app

@app.get("/")
def home():
    return {"message": "Funcionando corretamente!"}