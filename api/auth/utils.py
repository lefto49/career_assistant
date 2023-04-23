import random
import string
from jwt import decode

from django.core.exceptions import ObjectDoesNotExist

import career_assistant.settings
from api.models import User


def generate_code(length=10):
    return ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=length))


def get_user_from_token(token):
    token = token[7:]
    uid = decode(token, career_assistant.settings.SECRET_KEY, algorithms=['HS256'])['user_id']

    if not User.objects.filter(id=uid).exists():
        raise ObjectDoesNotExist

    return User.objects.get(id=uid)
