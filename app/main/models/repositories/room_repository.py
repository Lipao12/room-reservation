from psycopg2.extensions import connection
from typing import Dict, Tuple, List

class RoomRepository:
    def __init__(self, conn:connection) -> None:
        self.conn = conn

    def create_room(self, room_info: Dict) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            INSERT INTO room
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
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            DELETE FROM room WHERE id = %s
            ''', (room_id)
        )
        room = cursor.fetchall()
        return room
    
    def find_rooms(self)->List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM room
            '''
        )
        room = cursor.fetchall()
        return room
    
    def find_expecific_room(self, room_id)->List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM room WHERE id=%s
            ''',(room_id)
        )
        room = cursor.fetchall()
        return room