from main.server.server import app

if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run("main.server.server:app", reload=True)
