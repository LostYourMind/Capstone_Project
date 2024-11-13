import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import schedule

logger = logging.getLogger("UserService")

class UserService:
    def __init__(self, connection: Any):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def check_user_exists(self, device_id: str) -> bool:
        """device_id가 이미 users 테이블에 존재하는지 확인"""
        sql = "SELECT user_id FROM users WHERE user_id = %s"
        self.cursor.execute(sql, (device_id,))
        result = self.cursor.fetchone()
        return result is not None  # 존재하면 True, 없으면 False

    def create_user(self, device_id: str) -> bool:
        """Device ID와 timestamp를 users 테이블에 삽입 (이미 존재하면 삽입하지 않음)"""
        if self.check_user_exists(device_id):
            logger.info(f"Device ID {device_id} already exists in users table.")
            return True  # 이미 존재하면 True 반환
        sql = """
        INSERT INTO users(user_id, created_at)
        VALUES (%s, %s)
        """
        values = (device_id, datetime.now())  # 현재 시간을 삽입
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            logger.info(f"Device ID {device_id} and timestamp successfully inserted into users table.")
            return False  # 새로 삽입되었으므로 False 반환
        except Exception as e:
            self.connection.rollback()  # 삽입 실패 시 롤백
            logger.error(f"Failed to insert data into users table: {e}")
            raise

    def create_user_data(self, data: Dict):
        """user_data 테이블에 센서 데이터를 삽입"""
        sql = """
        INSERT INTO user_data (user_id, aver_heart_rate, Acetona, Alcohol, CO, CO2, NH4, Tolueno, 
                               temp, humi, led_value, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get("deviceId"),
            data.get("heartRate"),
            data.get("Acetona"),
            data.get("Alcohol"),
            data.get("CO"),
            data.get("CO2"),
            data.get("NH4"),
            data.get("Tolueno"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("led_value"),
            data.get("created_at", datetime.now())  # 기본값은 현재 시간
        )

        if len(values) != 12:
            raise ValueError("Not enough parameters for the SQL statement. Expected 12 values.")

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            logger.info("Sensor data successfully inserted into user_data table.")
        except Exception as e:
            self.connection.rollback()  # 삽입 실패 시 롤백
            logger.error(f"Failed to insert sensor data into user_data table: {e}")
            raise

    def get_bpm_values_by_device_id(self, device_id: str) -> List[float]:
        """
        특정 device_id에 해당하는 BPM 데이터를 user_data 테이블에서 조회하여 반환
        """
        sql = """
        SELECT aver_heart_rate 
        FROM user_data 
        WHERE user_id = %s
        ORDER BY created_at DESC
        """
        try:
            #logger.info(f"Executing SQL Query: {sql} with device_id={device_id}")
            self.cursor.execute(sql, (device_id,))
            results = self.cursor.fetchall()
            #logger.info(f"Query Results: {results}")

            # 튜플 리스트에서 값만 추출하여 리스트로 반환
            bpm_values = [float(row[0]) for row in results]
            #logger.info(f"Extracted BPM Values: {bpm_values}")
            return bpm_values

        except Exception as e:
            logger.error(f"Failed to retrieve BPM values for device_id {device_id}: {e}")
            raise

    def delete_user_data(self, data_id: int):
        """user_data 테이블에서 특정 데이터 삭제"""
        sql = "DELETE FROM user_data WHERE data_id = %s"
        try:
            self.cursor.execute(sql, (data_id,))
            self.connection.commit()
            logger.info(f"Data successfully deleted for data_id: {data_id}")
        except Exception as e:
            self.connection.rollback()  # 삭제 실패 시 롤백
            logger.error(f"Failed to delete data for data_id: {data_id}: {e}")
            raise
