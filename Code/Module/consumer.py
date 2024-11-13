# consumer.py
import pika
import json
import sys
import os

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from CRUD_FILE.Service import UserService
from Control.DBcontrol import dbControl


buffer = []  # 메시지를 저장할 버퍼
BATCH_SIZE = 5  # 버퍼에 쌓을 메시지 개수

def process_message(ch, method, properties, body):
    """RabbitMQ 큐에서 받은 메시지를 처리하고 일정 개수 이상 쌓이면 데이터베이스에 저장하는 함수"""
    data = json.loads(body)
    print(f" [x] Received {data}")

    buffer.append(data)

    # 버퍼가 BATCH_SIZE에 도달했을 때만 데이터베이스에 저장
    if len(buffer) >= BATCH_SIZE:
        db_connection = dbControl.initialize_db_connection()
        if db_connection:
            user_service = UserService(db_connection)
            try:
                for item in buffer:
                    # 먼저 device_id가 users 테이블에 있는지 확인
                    device_id = item.get("deviceId")
                    if not user_service.check_user_exists(device_id):
                        user_service.create_user(device_id)  # 새 사용자 생성

                    # 사용자 데이터를 user_data 테이블에 저장
                    user_service.create_user_data(item)

                db_connection.commit()  # 모든 항목이 저장된 후 커밋
                print("Batch data successfully saved in the database.")
            except Exception as e:
                db_connection.rollback()  # 에러 발생 시 롤백
                print(f"Failed to save batch data: {e}")
            finally:
                db_connection.close()
                buffer.clear()  # 버퍼 초기화
                ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print("Could not establish database connection.")
    else:
        # 데이터베이스 저장 없이 메시지만 처리 완료
        ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_from_queue():
    """RabbitMQ 큐로부터 메시지를 지속적으로 소비하는 함수"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sensor_data')
    channel.basic_consume(queue='sensor_data', on_message_callback=process_message)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume_from_queue()
