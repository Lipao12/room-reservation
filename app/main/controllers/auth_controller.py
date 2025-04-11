from fastapi import HTTPException
from passlib.hash import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Dict
import uuid

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

class UserAuthController:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, email: str, password: str):
        try:
                
            user = self.user_repository.find_by_email(email)
            if not user or not bcrypt.verify(password, user[3]):
                raise HTTPException(status_code=401, detail="Credenciais inválidas") # Teste para ver se é mais interessante

            token_data = {
                "sub": user[2], #email
                "exp": datetime.utcnow() + timedelta(hours=1)
            }
            user_data = {
                "id": user[0],
                "name": user[1]
            }

            token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
            return {
                'body':{"access_token": token, "user": user_data,"token_type": "bearer"},
                'status_code': 201
                }
        
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }

    def register(self, body:Dict):
        try:
            if self.user_repository.find_by_email(body["email"]):
                raise HTTPException(status_code=400, detail="E-mail já cadastrado") #
            
            id = str(uuid.uuid4())
            hashed_password = bcrypt.hash(body['password'])
            user_info={
                    "id": id,
                    "name":body["name"],
                    "email":body['email'],
                    "password":hashed_password
                }
            
            self.user_repository.create_user(user_info)
            return{
                    'body': {"user_id": id, "message": "Usuário registrado com sucesso"},
                    'status_code': 201
                }
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }