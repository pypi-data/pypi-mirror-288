import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# cffi-1.16.0 cryptography-43.0.0 pycparser-2.22

class ma_crystal:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.fernet = self._create_fernet(secret_key)


    def _generate_key(self, username):
        salt = username.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
        return Fernet(key)

    def generate_serial_key(self, username, start_date, end_date):
        f = self._generate_key(username)
        data = f"{start_date}|{end_date}".encode()
        return f.encrypt(data).decode()

    def validate_serial_key(self, username, serial_key):
        f = self._generate_key(username)
        try:
            decrypted_data = f.decrypt(serial_key.encode()).decode()
            start_date, end_date = decrypted_data.split('|')
            return start_date, end_date
        except:
            return None
    
    def validate_date(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            current = datetime.now()
            return start <= current <= end
        except ValueError:
            return False
    
    def generate_end_date(self, years=0, months=0, days=0):
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
        """
        Returns today's date in the format 'YYYY-MM-DD'.
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    def string_to_secret_key(self, input_string):
        """
        Converts a string to a secret key.
        """
        salt = b'salt_'  # You might want to use a more secure salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(input_string.encode()))
        return key.decode()

    def secret_key_to_string(self, secret_key, encrypted_string):
        """
        Attempts to decrypt the encrypted_string using the secret_key.
        Returns the original string if successful, otherwise returns None.
        """
        try:
            fernet = Fernet(secret_key.encode())
            decrypted = fernet.decrypt(encrypted_string.encode())
            return decrypted.decode()
        except:
            return None
    
    def _create_fernet(self, secret_key):
        salt = b'ma_crystal_salt'  # You might want to use a more secure salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
        return Fernet(key)

    def encrypt_string(self, input_string):
        """
        Encrypts the input string using the secret key.
        """
        encrypted = self.fernet.encrypt(input_string.encode())
        return encrypted.decode()

    def decrypt_string(self, encrypted_string):
        """
        Decrypts the encrypted string using the secret key.
        """
        try:
            decrypted = self.fernet.decrypt(encrypted_string.encode())
            return decrypted.decode()
        except:
            return None

    def encrypt_data(self, data):
        """
        Encrypts the input data (bytes).
        Returns the encrypted data as bytes.
        """
        return self.fernet.encrypt(data)

    def decrypt_data(self, encrypted_data):
        """
        Decrypts the encrypted data (bytes).
        Returns the decrypted data as bytes.
        """
        try:
            return self.fernet.decrypt(encrypted_data)
        except:
            return None

    

# Example usage
if __name__ == "__main__":
    secret_key = "your_secret_key_here"
    skm = ma_crystal(secret_key)

    # Generate a serial key
    username = "john_doe"
    start_date = "2023-07-01"
    end_date = "2023-12-31"
    serial_key = skm.generate_serial_key(username, start_date, end_date)
    print(f"Generated Serial Key: {serial_key}")

    # Validate the serial key
    validated_start, validated_end = skm.validate_serial_key(username, serial_key)
    print(f"Validated Start Date: {validated_start}")
    print(f"Validated End Date: {validated_end}")

    if skm.validate_date("2024-07-01","2024-12-31"):
        print("validated date")
    else:
        print("in-validate date")

    print("today : ", skm.get_today_date())

    print(skm.generate_end_date(0,0,1))
    print(skm.generate_end_date(0,1,0))
    print(skm.generate_end_date(1,0,0))

    # Try with an invalid key
    invalid_result = skm.validate_serial_key(username, "invalid_key")
    print(f"Invalid Key Result: {invalid_result}")
    invalid_result = skm.validate_serial_key("wrong_name", secret_key)
    print(f"Invalid Key Result: {invalid_result}")

    # Test encryption
    original_string = "Hello, ma_crystal!"
    encrypted = skm.encrypt_string(original_string)
    print(f"Encrypted: {encrypted}")

    # Test decryption
    decrypted = skm.decrypt_string(encrypted)
    print(f"Decrypted: {decrypted}")

    # Test decryption with wrong key
    wrong_key = "wrong_secret_key"
    wrong_skm = ma_crystal(wrong_key)
    wrong_decryption = wrong_skm.decrypt_string(encrypted)
    print(f"Decryption with wrong key: {wrong_decryption}")


    # Encrypt a file
    input_filename = "example.bin"  # This can be any file, binary or text
    output_encrypted_filename = "example_encrypted.bin"

    # Read and encrypt the file
    with open(input_filename, "rb") as file:
        file_content = file.read()
    encrypted_content = skm.encrypt_data(file_content)

    # Save the encrypted content
    with open(output_encrypted_filename, "wb") as file:
        file.write(encrypted_content)

    print(f"File '{input_filename}' has been encrypted and saved as '{output_encrypted_filename}'")

    # Decrypt the file
    input_encrypted_filename = output_encrypted_filename  # Using the file we just encrypted
    output_decrypted_filename = "example_decrypted.bin"

    # Read and decrypt the file
    with open(input_encrypted_filename, "rb") as file:
        encrypted_content = file.read()
    decrypted_content = skm.decrypt_data(encrypted_content)

    if decrypted_content:
        # Save the decrypted content
        with open(output_decrypted_filename, "wb") as file:
            file.write(decrypted_content)
        print(f"File '{input_encrypted_filename}' has been decrypted and saved as '{output_decrypted_filename}'")
    else:
        print("Decryption failed. The file might be corrupted or the wrong key was used.")

