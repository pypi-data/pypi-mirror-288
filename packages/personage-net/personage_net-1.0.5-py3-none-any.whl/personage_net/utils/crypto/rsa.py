# utils/crypto/rsa
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
import os

# 配置密钥存储路径
KEYS_DIR = "keys"
private_key_path = os.path.join(KEYS_DIR, "private_key.pem")
public_key_path = os.path.join(KEYS_DIR, "public_key.pem")

os.makedirs(KEYS_DIR, exist_ok=True)
# 生成rsa秘钥对保存
def generate_rsa_key():
    # 生成 rsa 秘钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 将秘钥保存到pem文件中
    with open(private_key_path, 'wb') as private_key_file:
        private_key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # 保存公钥
    with open(public_key_path, 'wb') as public_key_file:
        public_key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

# 返回私钥，格式是utf8格式
def load_private_key(isStr = False):
    # 加载私钥
    with open(private_key_path, 'rb') as private_key_file:
        private_key_data = private_key_file.read()

    private_key = serialization.load_pem_private_key(
        private_key_data,
        password=None,  # 如果私钥是加密的，需要提供解密密码
        backend=default_backend()
    )

    if isStr:
        # 将私钥序列化为 PEM 格式的字节数据
        pem_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem_data.decode('utf-8').strip().replace('-----BEGIN PUBLIC KEY-----\n', '').replace('\n-----END PUBLIC KEY-----', '')
    else:
        return private_key


# 返回公钥，格式utf8
def load_public_key(isStr = False):
    # 加载公钥
    with open(public_key_path, 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read()
        )
    if isStr:
        # 将公钥序列化为 PEM 格式的字节数据
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem_data.decode('utf-8').strip().replace('-----BEGIN PUBLIC KEY-----\n', '').replace('\n-----END PUBLIC KEY-----', '')
    else:
        return public_key

# 私钥解码
def encrypted_decode_key(password):
    # 获取私钥
    private_key = load_private_key()
    try:
        # 解密 AES 密钥
        decrypted_aes_key = private_key.decrypt(
            base64.b64decode(password),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return decrypted_aes_key
    except ValueError as e:
        print("Decryption failed:", e)
        raise


