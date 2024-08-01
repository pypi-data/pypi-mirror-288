# coding = utf-8
# app/auth/routes.py
from fastapi import APIRouter, Depends
from aiomysql import Connection
from personage_net.db.connection import get_db_conn
from personage_net.models.user import User, Login
from personage_net.utils.response import response_result, error_message
from personage_net.utils.crypto.rsa import encrypted_decode_key
from personage_net.utils.crypto.aes import aes_decrypt
from personage_net.utils.crypto.bcrypt import check_password, hashed_password
router = APIRouter()

@router.get('/fast/getUserlist')
async def read_user_list(conn=Depends(get_db_conn)):
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM my_project.userinfo")
        result = await cursor.fetchall()
        if not result:
            return response_result(code=200, msg='查询成功', operation='查询用户列表')
        data = [{'name': row[1], 'id': row[0], 'username': row[2]} for row in result]
        return response_result(code=200, msg='查询成功', operation='查询用户列表', data=data)

@router.post('/fast/createUser')
async def save_user_info(user_info: User, conn: Connection = Depends(get_db_conn)):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT * from my_projct.useringo where username = {user_info.username}")
            result = await cursor.fetchall()
            if not result:
                await cursor.execute("INSERT INTO my_project.userinfo (name, username, password) VALUES (%s, %s, %s)",
                                     (user_info.name, user_info.username, user_info.password))
                return response_result(code=200, msg='用户创建成功', operation='创建用户')
            return response_result(code=1000, msg='用户名存在', operation='创建用户')
    except Exception as e:
        error_message(e)

@router.post('/fast/login')
async def user_login(LoginInfo: Login, conn: Connection = Depends(get_db_conn) ):
    # rsa私钥进行解密aes私钥
    aes_private_key = encrypted_decode_key(LoginInfo.AES)


    # aes跟IV反解密码跟账户
    aes_dispose_password = aes_decrypt(LoginInfo.password, aes_private_key, LoginInfo.IV)
    username = aes_decrypt(LoginInfo.username, aes_private_key, LoginInfo.IV)

    async with conn.cursor() as cursor:
        await cursor.execute("SELECT password FROM my_project.userinfo u where username = %s", username)
        result = await cursor.fetchone()
        if not result:
            return response_result(code=10002, msg='用户不存在', operation='用户登录')
        if check_password(result[0], aes_dispose_password):
            return response_result(code=200, msg='登录成功', operation='用户登录', userInfo = {"token":'111122'})
        else:
            return response_result(code=10001, msg='密码或用户名有误，请检查后重新输入', operation='用户登录')

