# cython: language_level=3
# distutils: language = c++

import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

cdef class ma_crystal:
    cdef str secret_key
    cdef object fernet

    def __init__(self, str secret_key):
        self.secret_key = secret_key
        self.fernet = self._create_fernet(secret_key)

    cdef object _create_fernet(self, str secret_key):
        salt = b'ma_crystal_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
        return Fernet(key)

    cdef object _generate_key(self, str username):
        salt = username.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
        return Fernet(key)

    def generate_serial_key(self, str username, str start_date, str end_date):
        f = self._generate_key(username)
        data = f"{start_date}|{end_date}".encode()
        return f.encrypt(data).decode()

    def validate_serial_key(self, str username, str serial_key):
        f = self._generate_key(username)
        try:
            decrypted_data = f.decrypt(serial_key.encode()).decode()
            start_date, end_date = decrypted_data.split('|')
            return start_date, end_date
        except:
            return None

    def validate_date(self, str start_date, str end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            current = datetime.now()
            return start <= current <= end
        except ValueError:
            return False

    def generate_end_date(self, int years=0, int months=0, int days=0):
        today = datetime.now()
        end_date = today + timedelta(days=days)
        
        # Adding months and years
        end_date = end_date.replace(year=end_date.year + years)
        month = end_date.month + months
        year = end_date.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        try:
            end_date = end_date.replace(year=year, month=month)
        except ValueError:
            # Handle cases where the day doesn't exist in the target month
            end_date = end_date.replace(year=year, month=month, day=1) - timedelta(days=1)
        
        return end_date.strftime("%Y-%m-%d")

    def get_today_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def string_to_secret_key(self, str input_string):
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(input_string.encode()))
        return key.decode()

    def secret_key_to_string(self, str secret_key, str encrypted_string):
        try:
            fernet = Fernet(secret_key.encode())
            decrypted = fernet.decrypt(encrypted_string.encode())
            return decrypted.decode()
        except:
            return None

    def encrypt_string(self, str input_string):
        encrypted = self.fernet.encrypt(input_string.encode())
        return encrypted.decode()

    def decrypt_string(self, str encrypted_string):
        try:
            decrypted = self.fernet.decrypt(encrypted_string.encode())
            return decrypted.decode()
        except:
            return None

    def encrypt_data(self, bytes data):
        return self.fernet.encrypt(data)

    def decrypt_data(self, bytes encrypted_data):
        try:
            return self.fernet.decrypt(encrypted_data)
        except:
            return None