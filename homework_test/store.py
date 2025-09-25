import time
import json
import logging
from functools import wraps
from redis import ConnectionError, TimeoutError, Redis

logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

class Store:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.max_retries_conn = 3
        self.timeout = 3  # seconds
        self.connection = None

    def retry(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = self.max_retries_conn
            while retries > 0:
                try:
                    if not self.connection:
                        self.connection = self.connect()
                    result = func(self, *args, **kwargs)
                    return result
                except (ConnectionError, TimeoutError) as err:
                    retries -= 1
                    logging.info("Connection error occurred: %s Retrying (%s attempts left)...", err, retries)
                    time.sleep(1)

            raise TimeoutError("Maximum number of retries exceeded.")

        return wrapper

    def connect(self):
        """Создаем соединение с Redis"""
        try:
            connection = Redis(host=self.host, port=self.port, db=self.db, socket_timeout=self.timeout)
            connection.ping()  # проверяем доступность сервера
            return connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis server: {e}")

    def cache_get(self, key):
        """
        Получаем значение из кеша Redis.
        Возвращает строку или None, если ключ отсутствует.
        """
        try:
            self.connection = self.connect()
            value = self.connection.get(key)
        except Exception as e:
            value = None
        return value.decode('utf-8') if value else None

    def cache_set(self, key, value, expire_time=60):
        """
        Устанавливаем значение в кэш Redis с временем истечения.
        """
        try:
            self.connection = self.connect()
            self.connection.setex(key, expire_time, value)
        except Exception:
            pass

    @retry
    def get(self, key):
        """
        Получаем значение по ключу из Redis.
        Возвращает строковое представление значения или None, если ключ не найден.
        """
        value = self.connection.get(key)
        return value.decode('utf-8') if value else None

    @retry
    def set(self, key, value):
        """
        Устанавливаем ключ и значение в Redis.
        """
        self.connection.set(key, json.dumps(value))
