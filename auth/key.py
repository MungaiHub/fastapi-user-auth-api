import secrets


SECRET_KEY = secrets.token_hex(32)  # Generate a secure random secret key
print(SECRET_KEY)