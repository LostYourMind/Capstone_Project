import sys
import os


from sqlalchemy.orm import Session
from sqlalchemy import text


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


### 심박수 데이터 저장 코드 수정 필요
def call_select_all_kiosk(db: Session, user_id: str):
    stmt = text("CALL SelectAllKiosk(:user_id)")
    params = {"user_id": user_id}
    result = db.execute(stmt, params)
    return result.fetchall()
