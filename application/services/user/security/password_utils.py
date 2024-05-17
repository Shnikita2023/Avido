import bcrypt


def hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def compare_passwords(
        password: str,
        hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
