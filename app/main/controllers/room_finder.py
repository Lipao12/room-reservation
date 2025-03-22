from datetime import datetime, timedelta
from typing import Dict

class RoomFinder:
    def __init__(self, room_repository) -> None:
        self.room_repository = room_repository

    def find_all(self)->Dict:
        try:
            rooms = self.room_repository.find_rooms()
            if not rooms:
                return {
                    "body": {"error": "Sala não encontrada"},
                    "status_code": 404
                }
            rooms_info = [
                        {
                            "id": room[0], 
                            "name": room[1], 
                            "capacity": room[2]
                        } for room in rooms
                    ]
            return {
                "body": {"room": rooms_info, },
                "status_code": 200
                } 
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }

    def find_one(self, room_id)->Dict:
        try:
            room = self.room_repository.find_expecific_room(room_id)
            print(room)
            if not room:
                return {
                    "body": {"error": "Sala não encontrada"},
                    "status_code": 404
                }
            room_info = {
                "id": room[0], 
                "name": room[1], 
                "capacity": room[2], 
            }
            return {
                "body": {"room": room_info, },
                "status_code": 200
                } 
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }