# coding = utf-8
# app/utils/routes.py
from fastapi import APIRouter
from personage_net.utils.crypto.rsa import generate_rsa_key ,load_public_key, private_key_path, public_key_path
from personage_net.utils.response import response_result, error_message
import os

router = APIRouter()

# 获取rsa的公钥
@router.get('/fast/getRsaKey')
async def get_rsa_key():
    try:
        # 检查 RSA 密钥文件是否存在
        if not (os.path.exists(private_key_path) and os.path.exists(public_key_path)):
            # 如果密钥文件不存在，则生成新的 RSA 密钥
            generate_rsa_key()
        # 加载 RSA 密钥
        public_key = load_public_key(True)

        # 返回成功响应，包含公钥
        return response_result(code=200, msg='操作成功', operation='查询rsa公钥', key=public_key)
    except Exception as e:
        # 捕获所有异常并处理
        error_message(e)