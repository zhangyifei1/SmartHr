from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(
    data: Any = None,
    msg: str = "success",
    code: int = 200,
    status_code: int = 200
) -> JSONResponse:
    """
    成功响应
    :param data: 响应数据
    :param msg: 响应消息
    :param code: 业务状态码
    :param status_code: HTTP状态码
    :return: JSONResponse
    """
    content = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return JSONResponse(content=content, status_code=status_code)

def error_response(
    msg: str = "error",
    code: int = 400,
    data: Any = None,
    status_code: int = 400
) -> JSONResponse:
    """
    错误响应
    :param msg: 错误消息
    :param code: 业务状态码
    :param data: 响应数据
    :param status_code: HTTP状态码
    :return: JSONResponse
    """
    content = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return JSONResponse(content=content, status_code=status_code)
