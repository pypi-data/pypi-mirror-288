
from marearts_crystal import ma_crystal

secret_key = "marearts_anpr_rlawjdgus!23"
skm = ma_crystal(secret_key)

# Generate a serial key
username = "hello@marearts.com"
start_date = skm.get_today_date()
end_date = skm.generate_end_date(0,0,1) #year, month, day

serial_key = skm.generate_serial_key(username, start_date, end_date)
print(f"Generated Serial Key: {serial_key}")

# Validate the serial key
validated_start, validated_end = skm.validate_serial_key(username, serial_key)
print(f"Validated Start Date: {validated_start}")
print(f"Validated End Date: {validated_end}")

#date validateion
if skm.validate_date(validated_start, validated_end):
    print("validated date")
else:
    print("in-validate date")