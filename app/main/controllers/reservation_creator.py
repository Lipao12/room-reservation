import uuid
from typing import Dict
from datetime import datetime
from fastapi import HTTPException

class ReservationCreator:
    def __init__(self, reservation_repository) -> None:
        self.reservation_repository = reservation_repository
    
    def create(self, body)->Dict:
        try:
            
            conflicting_reservations = self.reservation_repository.check_availability(room_id=body["room_id"],
                                                                                  date=body['date'],
                                                                                  start_time=body['start_time'],
                                                                                  end_time=body['end_time'])
            if conflicting_reservations:
                raise HTTPException(status_code=400, detail="A sala já está reservada nesse horário.")

            id = str(uuid.uuid4())
            date = datetime.strptime(body['date'], "%Y-%m-%d").date()
            start_time = datetime.strptime(body['start_time'], "%H:%M:%S").time()
            end_time = datetime.strptime(body['end_time'], "%H:%M:%S").time()
            reservation_info={
                "id": id,
                "user_id":body["user_id"],
                "room_id":body['room_id'],
                "date":date,
                "start_time":start_time,
                "end_time":end_time,
                "status":body['status'],
            }

            self.reservation_repository.create_reservation(reservation_info)
            return{
                'body': {"reservation": reservation_info, "reservation_id":id},
                'status_code': 201
            }

        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }
    
    def delete(self, reservation_id)->Dict:
        try:
            self.reservation_repository.delete_reservation(reservation_id)
            return{
                'body': {"reservation_id": reservation_id, "message": "Deletado com sucesso!"},
                'status_code': 201
            }

        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }