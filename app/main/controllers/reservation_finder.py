from datetime import datetime, timedelta
from typing import Dict

class ReservationFinder:
    def __init__(self, reservation_repository) -> None:
        self.reservation_repository = reservation_repository

    def _format_date(self, date_value) -> str:
        """Converte objetos de data para string no formato 'YYYY-MM-DD'."""
        if isinstance(date_value, datetime):
            return date_value.strftime("%Y-%m-%d") 
        elif isinstance(date_value, str):
            return date_value  
        return str(date_value) 

    def find_by_user(self, user_id: str)->Dict:
        try:
            reservations = self.reservation_repository.get_reservations_by_user(user_id)
            if not reservations:
                return {
                    "body": {"error": "Não há reservas para esse usuário!"},
                    "status_code": 404
                }
            reservations_info = [
                        {
                            "id": reservation[0], 
                            "room_id": reservation[2],
                            "date": self._format_date(reservation[3]),
                            "start_time": str(reservation[4]), 
                            "end_time": str(reservation[5]),
                            "status": reservation[6],
                        } for reservation in reservations
                    ]
            print(reservations_info)
            return {
                "body": {"reservations": reservations_info, },
                "status_code": 200
                } 
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }

    def find_by_room(self, room_id: str)->Dict:
        try:
            reservations = self.reservation_repository.get_reservations_by_room(room_id)
            if not reservations:
                return {
                    "body": {"error": "Não há reservas para essa sala!"},
                    "status_code": 404
                }
            reservations_info = [
                        {
                            "id": reservation[0], 
                            "user_id": reservation[1],
                            "date": self._format_date(reservation[3]),
                            "start_time": str(reservation[4]), 
                            "end_time": str(reservation[5]),
                            "status": reservation[6],
                        } for reservation in reservations
                    ]
            return {
                "body": {"reservations": reservations_info, },
                "status_code": 200
                } 
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }
        
    def find_by_id(self, reservation_id: str)->Dict:
        try:
            reservation = self.reservation_repository.get_reservation_by_id(reservation_id)
            if not reservation:
                return {
                    "body": {"error": "Sala não encontrada"},
                    "status_code": 404
                }
            reservation_info = {
                            "id": reservation[0], 
                            "user_id": reservation[1], 
                            "room_id": reservation[2],
                            "date": self._format_date(reservation[3]),  
                            "start_time": str(reservation[4]), 
                            "end_time": str(reservation[5]),
                            "status": reservation[6],
                        } 
            return {
                "body": {"reservation": reservation_info, },
                "status_code": 200
                } 
        except Exception as exception:
            return{
                "body":{"error":"Bad Request", "message":str(exception)},
                "status_code":400
            }