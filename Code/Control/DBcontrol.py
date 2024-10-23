import logging
import os
import sys

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from CRUD_FILE.db_connection import connect_to_db
from CRUD_FILE.Service import UserService

logger = logging.getLogger("DBControl")

class dbControl:
    
    @staticmethod
    def initialize_db_connection():
        """데이터베이스 연결을 초기화하는 함수"""
        connection = connect_to_db()
        if connection is None:
            logger.error("Failed to connect to the database.")
            return None
        return connection

    @staticmethod
    def close_db_connection(connection):
        """데이터베이스 연결을 종료하는 함수"""
        if connection:
            connection.close()
            logger.info("Database connection closed.")

    @staticmethod
    def create_user_and_data(name, heart_rate, temp, humi, air_condition, led_value):
        """사용자 및 관련 데이터 생성"""
        connection = dbControl.initialize_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                service = UserService(cursor)
                user_id = service.create_user_with_data(name, heart_rate, temp, humi, air_condition, led_value)
                connection.commit()
                logger.info(f"User {name} and related data created with ID {user_id}.")
            except Exception as e:
                connection.rollback()
                logger.error(f"Error occurred while creating user and data: {e}")
            finally:
                cursor.close()
                dbControl.close_db_connection(connection)

    @staticmethod
    def get_user_and_data(user_id):
        """사용자 및 관련 데이터 조회"""
        connection = dbControl.initialize_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                service = UserService(cursor)
                user_data = service.get_user_and_data(user_id)
                logger.info(f"User and related data for ID {user_id} fetched successfully.")
                return user_data
            except Exception as e:
                logger.error(f"Error occurred while fetching user and data: {e}")
            finally:
                cursor.close()
                dbControl.close_db_connection(connection)
