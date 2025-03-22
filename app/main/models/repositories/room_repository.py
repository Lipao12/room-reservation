from psycopg2.extensions import connection
from typing import Dict, Tuple, List

class RoomRepository:
    def __init__(self, conn:connection) -> None:
        self.conn = conn

    def create_room(self, room_info: Dict) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO rooms
                    (id, name, capacity)
                VALUES
                    (%s, %s, %s)
                ''',
                (
                    room_info["id"],
                    room_info["name"],
                    room_info["capacity"],
                )
            )
        self.conn.commit()

    def delete_room(self, room_id: str)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                DELETE FROM rooms WHERE id = %s
                ''', (room_id,)
            )
        self.conn.commit()
    
    def find_rooms(self)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM rooms
                '''
            )
            rooms = cursor.fetchall()
        return rooms
    
    def find_expecific_room(self, room_id)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM rooms WHERE id=%s
                ''',(room_id,)
            )
            room = cursor.fetchone()
        return room