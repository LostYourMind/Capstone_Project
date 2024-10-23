### Service.py


from CRUD_FILE.crud_Operation import CRUDOperations

class UserService:
    def __init__(self, cursor):
        self.crud = CRUDOperations(cursor)

    def create_user_with_data(self, name, heart_rate, temp, humi, air_condition, led_value):
        """사용자 생성과 동시에 사용자 데이터를 삽입"""
        user_id = self.crud.create_user(name)
        self.crud.create_user_data(user_id, heart_rate, temp, humi, air_condition, led_value)
        return user_id

    def get_user_and_data(self, user_id):
        """사용자 및 관련 데이터 조회"""
        user_data = self.crud.read_user_data(user_id)
        return user_data

    def update_user_and_data(self, user_id, new_name, data_id, heart_rate, temp, humi, air_condition, led_value):
        """사용자와 관련 데이터를 업데이트"""
        self.crud.update_user_name(user_id, new_name)
        self.crud.update_user_data(data_id, heart_rate, temp, humi, air_condition, led_value)

    def delete_user_and_data(self, user_id):
        """사용자와 관련 데이터를 삭제"""
        self.crud.delete_user(user_id)
