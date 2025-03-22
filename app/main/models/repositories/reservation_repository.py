from psycopg2.extensions import connection
from typing import Dict, Tuple, List
from datetime import date, time


class ReservationRepository:
    def __init__(self, conn:connection) -> None:
        self.conn = conn
    
    def create_reservation(self, reservation_info: Dict)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO reservation
                    (id, user_id, room_id, date, start_time, end_time, status)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                ''',(reservation_info["id"], reservation_info["user_id"],reservation_info["room_id"], 
                     reservation_info["date"], reservation_info["start_time"], reservation_info["end_time"], 
                     reservation_info["status"],)
            )
            self.conn.commit()
          
    def update_reservation_status(self, reservation_id: str, status: str):
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE reservasion
                SET status=%s
                WHERE id=%s
                ''', (status, reservation_id,)
            )
            self.conn.commit()

    def delete_reservation(self, reservation_id: str)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                DELETE FROM reservation WHERE id = %s
                ''', (reservation_id,)
            )
            self.conn.commit()

    def check_availability(self, room_id: str, date: str, start_time: str, end_time: str)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT id FROM reservation 
                    WHERE room_id=%s 
                    AND date=%s
                    AND (
                        (start_time < %s AND end_time > %s) OR  -- O novo horário começa antes e termina depois
                        (start_time < %s AND end_time > %s) OR  -- O novo horário começa durante um horário reservado
                        (start_time >= %s AND start_time < %s) OR  -- O novo horário começa durante um horário reservado
                        (end_time > %s AND end_time <= %s)       -- O novo horário termina durante um horário reservado
                    )
                ''', (room_id, date, end_time, start_time, start_time, end_time, start_time, end_time, start_time, end_time,)
        )
            conflicting_reservations = cursor.fetchall()
            print("Conflitos: ", conflicting_reservations)
            if conflicting_reservations:
                return True
            return False

    def get_reservations_by_user(self, user_id: str) -> List:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM reservation WHERE user_id=%s
                ''', (user_id,)
            )
            rooms = cursor.fetchall()
        return rooms
    
    def get_reservation_by_id(self, reservation_id: str) -> List:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM reservation WHERE id=%s
                ''', (reservation_id,)
            )
            rooms = cursor.fetchone()
        return rooms
