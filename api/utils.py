import random
import string
from jwt import decode

from django.core.exceptions import ObjectDoesNotExist

import career_assistant.settings
from .RecomendSystem import getRecomendation
from .models import Vacancy, Cup, Course, User

def generate_code(length=10):
    return ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=length))

def set_recommendations(user):
    user.vacancies.clear()
    user.cups.clear()
    user.courses.clear()

    vacancies = getRecomendation(user.experience, 10, 'vacancy')
    for id in vacancies['id']:
        if Vacancy.objects.filter(id=id).exists():
            user.vacancies.add(Vacancy.objects.get(id=id))

    cups = getRecomendation(user.experience, 5, 'cup')
    for id in cups['id']:
        if Cup.objects.filter(id=id).exists():
            user.cups.add(Cup.objects.get(id=id))

    course = getRecomendation(user.experience, 3, 'course')
    for id in course['id']:
        if Course.objects.filter(id=id).exists():
            user.courses.add(Course.objects.get(id=id))

    user.save()

def get_user_from_token(token):
    token = token[7:]
    uid = decode(token, career_assistant.settings.SECRET_KEY, algorithms=['HS256'])['user_id']

    if not User.objects.filter(id=uid).exists():
        raise ObjectDoesNotExist

    return User.objects.get(id=uid)
