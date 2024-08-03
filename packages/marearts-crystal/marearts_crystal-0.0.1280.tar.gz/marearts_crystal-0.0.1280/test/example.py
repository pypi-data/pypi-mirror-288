
from marearts_crystal import ma_crystal

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

#date validateion
if skm.validate_date("2024-07-01","2024-12-31"):
    print("validated date")
else:
    print("in-validate date")

#get today date
print("today : ", skm.get_today_date())

#generate date by period
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
