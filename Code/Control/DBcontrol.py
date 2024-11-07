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

    
    def Find_heart_rate(self, deviceId:str) :
        result = self.crud.get_bpm_values_by_device_id(deviceId)
        #logging.info(f"Find_heart_rate data : {result}")
        return result


    
