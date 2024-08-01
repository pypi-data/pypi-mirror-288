# utils/crypto/aes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64


# aes解密
def aes_decrypt(encrypted_text, private_key, iv):
    private_key_byte = base64.b64decode(private_key)
    iv_byte_value = base64.b64decode(iv)
    encrypted_text_byte = base64.b64decode(encrypted_text)

    # 创建解密aes对象
    cipher = Cipher(algorithms.AES(private_key_byte), modes.CBC(iv_byte_value), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        # 解密
        padded_plain_text = decryptor.update(encrypted_text_byte) + decryptor.finalize()
        # 去除解密后的填充
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()
        return plain_text.decode('utf-8')
    except ValueError as e:
        print(f'aes解密错误{e}')
        raise




