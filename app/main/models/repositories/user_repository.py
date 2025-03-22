from psycopg2.extensions import connection
from typing import Dict, Tuple, List


class UserRepository:
    def __init__(self, conn:connection) -> None:
        self.conn = conn
    
    def find_by_email(self, email)->List[Tuple]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM users WHERE email=%s
                ''',(email,)
            )
            rooms = cursor.fetchone()
        return rooms
    
    def create_user(self, user_info: Dict):
        with self.conn.cursor() as cursor:

            cursor.execute(
                '''
                INSERT INTO users
                    (id, name, email, password)
                VALUES
                    (%s, %s, %s, %s)
                ''',(user_info["id"], user_info["name"], user_info["email"], user_info["password"])
            )
            self.conn.commit()
