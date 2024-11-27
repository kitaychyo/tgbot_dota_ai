import psycopg2
from psycopg2 import sql
hostname = 'localhost'  # или IP-адрес сервера
port = '5432'           # порт по умолчанию
username = 'postgres'  # ваше имя пользователя
password = '1234'  # ваш пароль
database = 'data'  # имя базы данных
class DBHandler:
    def __init__(self):

        try:
            self.conn = psycopg2.connect(
                host=hostname,
                port=port,
                user=username,
                password=password,
                dbname=database
            )
            self.cursor = self.conn.cursor()
            self._create_table()
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def _create_table(self):

        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_messages (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            username TEXT,
            message_text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка создания таблицы: {e}")

    def save_message(self, user_id, username, message_text):

        insert_query = """
        INSERT INTO user_messages (user_id, username, message_text)
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(insert_query, (user_id, username, message_text))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка сохранения сообщения: {e}")

    def close(self):

        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(f"Ошибка при закрытии соединения с базой данных: {e}")
