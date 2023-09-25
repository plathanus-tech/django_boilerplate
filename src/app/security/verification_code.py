import random
import string


def generate_numeric_verification_code(length: int):
    return "".join(random.choices(string.digits, k=length))  # nosec B311
