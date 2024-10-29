import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="app_logs.txt", max_bytes=1_000_000, backup_count=3):
    """로그 설정을 구성하는 함수"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count),
            logging.StreamHandler()  # 콘솔에도 로그 출력
        ]
    )
    logging.info("Logging is set up.")  # 설정 완료 메시지 로그
    