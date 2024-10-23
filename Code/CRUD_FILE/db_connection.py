import mysql.connector
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Database")


def connect_to_db():
    """MySQL 데이터베이스 연결을 담당하는 함수"""
    try:
        connection = mysql.connector.connect(
            host="localhost",           # MySQL 서버의 호스트
            port=3315,                  # 포트 번호 추가
            user="fastAPI",             # MySQL 사용자 이름
            password="redfox1774!",     # MySQL 비밀번호
            database="caps2",           # 사용할 데이터베이스 이름
        )
        if connection.is_connected():
            # print("Successfully connected to the database")
            logging.info("Successfully connected to the database")
            return connection  # 연결 객체 반환
    except mysql.connector.Error as err:
        # print(f"Error: {err}")
        logging.info(f"Error ocurt: {err}")
        return None  # 연결 실패 시 None 반환

