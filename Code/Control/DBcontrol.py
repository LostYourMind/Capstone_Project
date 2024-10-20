import os
import sys
import logging
from fastapi import Depends
from sqlalchemy.orm import Session

from CRUD_FILE.db_connection import connect_to_db

# 로그 설정
logger = logging.getLogger("DBControl")

# 현재 파일의 디렉토리를 모듈 검색 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# DataBase
db_connection = None


class dbControl:

    def initialize_db_connection():
        """데이터베이스 연결을 초기화하는 함수"""
        global db_connection
        db_connection = connect_to_db()
        if db_connection is None:
            logger.info("Failed to connect to the database.")
            return None

    def close_db_connection():
        """데이터베이스 연결을 종료하는 함수"""
        global db_connection
        if db_connection is not None:
            db_connection.close()
            logger.info("Database connection closed.")
