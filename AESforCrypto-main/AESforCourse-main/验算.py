import numpy as np
from Crypto.Cipher import AES
import os

# 转换密钥
key = os.urandom(16)
key_hex = ''.join(f'{byte:02X}' for byte in key)

# 转换明文
plaintext = os.urandom(16)
plaintext_hex = ''.join(f'{byte:02X}' for byte in plaintext)


# 创建 AES 加密器
cipher = AES.new(key, AES.MODE_ECB)

# 执行加密
ciphertext_bytes = cipher.encrypt(plaintext)

# 将加密结果转换为16进制
ciphertext  = ''.join(f'{byte:02X}' for byte in ciphertext_bytes)

print(f"密钥 (16进制): {key_hex}")
print(f"明文 (16进制): {plaintext_hex}")
print(f"密文 (16进制): {ciphertext}")