# CRUD 작업을 담당하는 모듈
def create_user(cursor, name, age):
    """Create: 새 사용자 데이터를 삽입"""
    sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
    values = (name, age)
    cursor.execute(sql, values)


def read_users(cursor):
    """Read: 모든 사용자 데이터를 조회"""
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    return cursor.fetchall()


def update_user_age(cursor, user_id, new_age):
    """Update: 특정 사용자의 나이를 업데이트"""
    sql = "UPDATE users SET age = %s WHERE id = %s"
    values = (new_age, user_id)
    cursor.execute(sql, values)


def delete_user(cursor, user_id):
    """Delete: 특정 사용자를 삭제"""
    sql = "DELETE FROM users WHERE id = %s"
    value = (user_id,)
    cursor.execute(sql, value)
