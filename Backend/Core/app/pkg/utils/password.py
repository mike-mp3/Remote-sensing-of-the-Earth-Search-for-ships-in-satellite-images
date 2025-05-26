import bcrypt
from pydantic import SecretBytes, SecretStr


def hash_password(password: SecretStr) -> SecretBytes:
    password_bytes = password.get_secret_value().encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return SecretBytes(hashed)


def verify_password(
    plain_password: SecretStr,
    hashed_password: SecretBytes,
) -> bool:
    password_bytes = plain_password.get_secret_value().encode("utf-8")
    hashed_bytes = hashed_password.get_secret_value()
    return bcrypt.checkpw(password_bytes, hashed_bytes)
