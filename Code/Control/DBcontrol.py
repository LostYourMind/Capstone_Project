import os
import sys
import logging
from fastapi import Depends
from sqlalchemy.orm import Session

# 로그 설정
logger = logging.getLogger("DBControl")

# 현재 파일의 디렉토리를 모듈 검색 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 필요한 모듈 임포트
from CRUD_FILE.database_session import get_db
from CRUD_FILE.crud import call_select_all_kiosk


class dbControl:

    # FastAPI 의존성 주입 함수
    def get_db_control(db: Session = Depends(get_db)):
        return dbControl(db)
