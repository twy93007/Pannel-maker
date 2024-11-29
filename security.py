import hashlib
import json
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
    def encrypt_data(self, data):
        """加密数据"""
        json_data = json.dumps(data)
        encrypted_data = self.cipher_suite.encrypt(json_data.encode())
        return encrypted_data
        
    def decrypt_data(self, encrypted_data):
        """解密数据"""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
        
    def verify_data_integrity(self, data, signature):
        """验证数据完整性"""
        data_hash = hashlib.sha256(str(data).encode()).hexdigest()
        return data_hash == signature 