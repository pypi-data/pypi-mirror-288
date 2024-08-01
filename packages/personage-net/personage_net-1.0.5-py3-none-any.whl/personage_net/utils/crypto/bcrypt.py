# utils/crypto/bcrypt
import bcrypt

# 密码哈希
def hashed_password(password: str) -> str:
    """
    加密过程
    :param password: str
    :return: str
    """
    # 生成盐值
    salt = bcrypt.gensalt()

    # 使用盐值进和密码生成哈希
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# 哈希值比对
def check_password(stored_hashed_password: str, password: str) -> bool:
    """
       验证密码
       :param stored_hashed_password: str, 存储的哈希密码
       :param password: str, 用户输入的密码
       :return: bool, 验证结果
       """
    # 将存储的哈希密码转换为字节形式
    stored_hashed_password_bytes = stored_hashed_password.encode('utf-8')
    # 使用存储的哈希密码进行验证
    return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password_bytes)
