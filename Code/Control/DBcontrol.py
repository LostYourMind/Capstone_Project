import logging
from typing import Dict, Any
from CRUD_FILE.db_connection import connect_to_db
from CRUD_FILE.Service import UserService  # CRUD 기능을 포함한 서비스 클래스

logger = logging.getLogger("DBControl")

class dbControl:
    
    def __init__(self, connection: Any):
        self.connection = connection
        self.crud = UserService(connection)  # 데이터베이스 작업을 위한 UserService 인스턴스 생성

    @staticmethod
    def initialize_db_connection():
        """데이터베이스 연결을 초기화하는 함수"""
        connection = connect_to_db()
        if connection is None:
            logger.error("Failed to connect to the database.")
            return None
        logger.info("Database connection established successfully.")
        return connection

    @staticmethod
    def close_db_connection(connection):
        """데이터베이스 연결을 종료하는 함수"""
        if connection:
            connection.close()
            logger.info("Database connection closed successfully.")
        else:
            logger.warning("Attempted to close a non-existent connection.")

    def save_data(self, data: Dict):
        """특정 필드만 추출하여 데이터베이스에 저장"""

        # 필요한 필드만 추출
        device_id = data.get("deviceId")

        # 로그 출력으로 추출한 데이터 확인
        logger.info(f"Saving data - Device ID: {device_id}")

        # UserService를 통해 데이터 저장
        try:
            temp = self.crud.create_user(device_id)
            if(temp == True) : 
                self.crud.create_user_data(data)
        except Exception as e:
            logger.error(f"Failed to save data in user_data table: {e}")
            raise
