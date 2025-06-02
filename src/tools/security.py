from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password_str: str) -> str:
    return ph.hash(password_str)

def verify_password(hashed_password: str, input_password: str) -> bool:
    try:
        ph.verify(hashed_password, input_password)
        return True
    except Exception:
        return False
