import secrets
from pydantic import SecretStr

def generate_secure_code(digits: int) -> SecretStr:
    """Generate secure digit code"""
    if digits > 1024:
        raise ValueError("Secure code cannot be more than 1024 digits")
    return SecretStr(''.join(str(secrets.randbelow(10)) for _ in range(digits)))

def verify_secure_code(
    plain_code: SecretStr,
    real_code: SecretStr
) -> bool:
    return plain_code.get_secret_value() == real_code.get_secret_value()