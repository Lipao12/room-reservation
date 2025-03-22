import uuid
from typing import Dict

class RoomCreator:
    def __init__(self, room_repository) -> None:
        self.room_repository = room_repository
    
    def create(self, body)->Dict:
        try:
            id = str(uuid.uuid4())
            room_info={
                "id": id,
                "name":body["name"],
                "capacity":body['capacity']
            }

            self.room_repository.create_room(room_info)
            return{
                'body': {"room_id": id},
                'status_code': 201
            }

        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }
    
    def delete(self, room_id)->Dict:
        try:
            self.room_repository.delete_room(room_id)
            return{
                'body': {"room_id": id, "message": "Deletado com sucesso!"},
                'status_code': 201
            }

        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }