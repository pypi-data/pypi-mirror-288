# -*- coding: utf-8 -*-
# coding = utf-8
# 接口请求统一返回处理
from fastapi import HTTPException, status
from typing import Any, Dict, List, Union
from ..settings import logger

def response_result(data: Union[List[Any], Dict[str, Any], None] = None, msg: str = '操作成功', code: int = 200, operation: str = '默认操作', **kw) -> Dict[str, Any]:
    """
       封装统一返回结果的函数

       参数:
       data: 返回的数据, 默认是空列表
       msg: 返回的消息, 默认是 '操作成功'
       code: 自定义状态码, 默认是 200
       operation: 操作名称

       返回:
       一个包含 state, data 和 msg 的字典
       """
    if data is None:
        data = []
    if code == 200:
        logger.info(f'操作信息：{operation}，错误结果：{msg}’')
    else:
        logger.error(f'code: {code} 。错误信息：{operation} 。错误提示：{msg}')

    return {
        'state': 200,
        'data': {
            'code': code,
            'result': data or None,
            'msg': msg,
            **kw,
        }
    }

def error_message(e):
    # 如果出现任何异常，例如数据库连接问题或SQL执行问题，将抛出
    # HTTP
    # 500
    # 内部服务器错误
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return response_result(code=500, msg=str(e), operation='系统错误')