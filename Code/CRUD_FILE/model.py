# models.py

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from sqlalchemy import Table, Column, Integer, String
from CRUD_FILE.database import metadata

# 기존 테이블 이름이 'users'라고 가정합니다.
users = Table("users", metadata, autoload_with=metadata.bind)


# ORM 매핑을 위한 클래스 정의
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
