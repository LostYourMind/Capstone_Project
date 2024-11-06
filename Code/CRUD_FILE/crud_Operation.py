import uuid
from datetime import datetime
import random
import string

class CRUDOperations:

    def __init__(self, cursor):
        self.cursor = cursor

    def create_user_data(self, device_id: str):
        """특정 필드만 사용하여 user_data에 데이터 삽입"""
        sql = """
        INSERT INTO user_data (user_id, created_at)
        VALUES (%s, NOW())
        """
        values = (device_id)
        self.cursor.execute(sql, values)