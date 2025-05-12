import hashlib
import secrets
import binascii
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def hash_password(password: str) -> str:
    """Hash a password with salt using PBKDF2_HMAC"""
    salt = secrets.token_bytes(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return f"{binascii.hexlify(salt).decode()}:{binascii.hexlify(pw_hash).decode()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a password against stored hash"""
    salt_str, pw_hash_str = stored_password.split(':')
    salt = binascii.unhexlify(salt_str)
    pw_hash = binascii.unhexlify(pw_hash_str)
    
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    return new_hash == pw_hash