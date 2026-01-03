from .variables import *

TIME_ZONE = "Asia/Almaty"

DATABASE_URL = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'