from fastapi import HTTPException, status

class BusinessException(HTTPException):
    """业务异常基类"""
    def __init__(self, code: int, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message

# 通用异常定义
class UserNotFoundException(BusinessException):
    def __init__(self, message: str = "用户不存在"):
        super().__init__(code=404001, message=message)

class UserAlreadyExistsException(BusinessException):
    def __init__(self, message: str = "用户已存在"):
        super().__init__(code=400001, message=message)

class IncorrectUsernameOrPasswordException(BusinessException):
    def __init__(self, message: str = "用户名或密码错误"):
        super().__init__(code=400002, message=message)

class PermissionDeniedException(BusinessException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(code=403001, message=message, status_code=status.HTTP_403_FORBIDDEN)

class InvalidTokenException(BusinessException):
    def __init__(self, message: str = "无效的token"):
        super().__init__(code=401001, message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class FileTooLargeException(BusinessException):
    def __init__(self, message: str = "文件大小超过限制"):
        super().__init__(code=400003, message=message)

class InvalidFileTypeException(BusinessException):
    def __init__(self, message: str = "不支持的文件类型"):
        super().__init__(code=400004, message=message)

class ResourceNotFoundException(BusinessException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404002, message=message, status_code=status.HTTP_404_NOT_FOUND)
