import uuid
from datetime import datetime
import random
import string

class CRUDOperations:
    def __init__(self, cursor):
        self.cursor = cursor

    def generate_random_name(self, length=6):
        """임의의 문자열을 생성하여 사용자 이름으로 사용"""
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(length))

    def create_user(self):
        """Create: 새 사용자 데이터를 삽입"""
        user_id = str(uuid.uuid4())  # UUID를 생성하여 사용자 ID로 사용
        name = f"USER_{self.generate_random_name()}"  # 임의의 이름 생성 (USER_ + 6자리 무작위 문자열)
        created_at = datetime.now()

        sql = "INSERT INTO users (user_id, name, created_at) VALUES (%s, %s, %s)"
        values = (user_id, name, created_at)
        self.cursor.execute(sql, values)
        return user_id  # 생성된 사용자 ID를 반환

    def create_user_data(self, user_id, aver_heart_rate, temp, humi, air_condition, led_value):
        """Create: 사용자 데이터를 삽입"""
        created_at = datetime.now()
        sql = """
        INSERT INTO user_data (user_id, aver_heart_rate, temp, humi, air_condition, led_value, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (user_id, aver_heart_rate, temp, humi, air_condition, led_value, created_at)
        self.cursor.execute(sql, values)

    def read_users(self):
        """Read: 모든 사용자 데이터를 조회"""
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def read_user_data(self, user_id):
        """Read: 특정 사용자의 데이터를 조회"""
        sql = """
        SELECT u.user_id, u.name, d.aver_heart_rate, d.temp, d.humi, d.air_condition, d.led_value, d.created_at
        FROM users u
        JOIN user_data d ON u.user_id = d.user_id
        WHERE u.user_id = %s
        """
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()

    def update_user_name(self, user_id, new_name):
        """Update: 특정 사용자의 이름을 업데이트"""
        sql = "UPDATE users SET name = %s WHERE user_id = %s"
        values = (new_name, user_id)
        self.cursor.execute(sql, values)

    def update_user_data(self, data_id, aver_heart_rate, temp, humi, air_condition, led_value):
        """Update: 특정 사용자의 데이터를 업데이트"""
        sql = """
        UPDATE user_data
        SET aver_heart_rate = %s, temp = %s, humi = %s, air_condition = %s, led_value = %s
        WHERE data_id = %s
        """
        values = (aver_heart_rate, temp, humi, air_condition, led_value, data_id)
        self.cursor.execute(sql, values)

    def delete_user(self, user_id):
        """Delete: 특정 사용자를 삭제"""
        # 먼저 user_data를 삭제해야 함 (외래키 제약 조건 때문에)
        sql_data = "DELETE FROM user_data WHERE user_id = %s"
        self.cursor.execute(sql_data, (user_id,))

        # 사용자 삭제
        sql_user = "DELETE FROM users WHERE user_id = %s"
        self.cursor.execute(sql_user, (user_id,))
