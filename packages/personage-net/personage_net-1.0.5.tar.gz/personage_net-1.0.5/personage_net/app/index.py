# coding = utf-8
# app/index.py
from fastapi import FastAPI
from .auth.routes import router as auto_router
from .utils.routes import router as utils_router
from personage_net.db.connection import init_db_pool, close_db_pool
import configparser
import os

def create_app() -> FastAPI:
    app = FastAPI()

    # ��ȡ��ǰ����Ŀ¼
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '../db/config.ini')

    # ���� configparser ����
    db_config = configparser.ConfigParser()
    db_config.read(config_path)

    DB_HOST = db_config['DATABASE']['DB_HOST']
    DB_PORT = db_config.getint('DATABASE', 'DB_PORT')
    DB_USER = db_config['DATABASE']['DB_USER']
    DB_PASSWORD = db_config['DATABASE']['DB_PASSWORD']
    DB_NAME = db_config['DATABASE']['DB_NAME']

    # �����¼�
    @app.on_event('startup')
    async def startup():
        await init_db_pool(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

    # �ر��¼�
    @app.on_event('shutdown')
    async def shutdown():
        await close_db_pool()

    # ע��·��
    app.include_router(auto_router, tags=['auth'])
    app.include_router(utils_router, tags=['utils'])

    return app
