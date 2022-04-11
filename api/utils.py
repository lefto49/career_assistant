import random
import string


def generate_code(length=10):
    return ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=length))
