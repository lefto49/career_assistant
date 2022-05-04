import operator
import pandas as pd
import numpy as np
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import Vacancy, Cup, Course


# "jobs.xlsx" - название файла с данными о вакансиях
# "courses.xlsx" - название файла с данными о вакансиях
# "cups.xlsx" - название файла с данными о вакансиях

def preprocess(text):
    tokenizer = TweetTokenizer()
    return ' '.join(tokenizer.tokenize(text.lower()))


def removePreinfo(text):
    for i in range(len(text)):
        if text[i] == ']':
            return text[i + 2:]
    return text


def removeMarks(text):
    return text.replace(',', "").replace('.', "").replace('/', "").replace('-', "") \
        .replace('[', "").replace(']', "").replace('(', "").replace(')', "") \
        .replace('»', "").replace('«', "").replace('—', "").replace('>', "").replace('<', "")


def clearText(text):
    return preprocess(removeMarks(removePreinfo(text)))


# Метод возвращающий DataFrame с рекомендованными позициями
def getRecomendation(text, recommendation_length, type):
    # Открываем данные о всех вакансиях
    if type == 'vacancy':
        data = pd.DataFrame.from_records(Vacancy.objects.all().values())
    elif type == 'cup':
        data = pd.DataFrame.from_records(Cup.objects.all().values())
    elif type == 'course':
        data = pd.DataFrame.from_records(Course.objects.all().values())

    columns_length = len(data.columns)

    # Чистим текст от лишних слов и ставим пробелы
    text = clearText(text)

    # Очищаем данные с пустым детальным описанием
    clear_data = data[data['description'].notna()]
    clear_data_length = len(clear_data['description'])

    # Помещаем заданный текст в данные
    clear_data.loc[len(data)] = text

    # Берем столбец с детальным описанием и предпроцессим его
    X = clear_data['description'].apply(clearText)

    # Получаем векторизатор и векторизуем данные с текстом пользователя
    tfidf_vect = TfidfVectorizer(max_features=5000)
    X_tfidf = tfidf_vect.fit_transform(X)

    # Полученные векторы нужно сравнить с текстом нашего пользователя
    # Выберем 10 ближайших описания и предложим пользователю
    # Векторы преобразуем в массив
    vectors = X_tfidf.toarray()

    # Создаем столбец, где будут храниться векторизованное описание каждой позиции
    zero_vect = [0] * (clear_data_length + 1)
    clear_data.insert(columns_length, "Векторы описания", zero_vect, True)

    # Здесь мы переинициализируем индексы, ибо они не упорядочены
    index_array = [0] * (clear_data_length + 1)
    for i in range(clear_data_length + 1):
        index_array[i] = i
    clear_data.reset_index(drop=True, inplace=True)

    # Считаем расстояние между векторами описаний позиций и вектором текста пользователя
    distance_array = []
    current_vector = np.array(vectors[len(vectors) - 1])
    for i in range(clear_data_length):
        vector = np.array(vectors[i])
        dist = np.linalg.norm(current_vector - vector)
        distance_array.append(dist)

    # Перемещаем расстояния в словарь, где ключ - индекс, а значение - расстояние позиции данных
    distances_with_indexes = {}
    for i in range(clear_data_length):
        distances_with_indexes[i] = distance_array[i]

    # Запишем индексы ближайших соседей
    indexes = []
    dictionary = distances_with_indexes
    for i in range(recommendation_length):
        index_of_min = min(dictionary.items(), key=operator.itemgetter(1))[0]
        indexes.append(index_of_min)
        dictionary.pop(index_of_min)

    # Создание пустого датафрейма с теми же колонками
    result = clear_data.copy().iloc[0:0]
    for i in range(recommendation_length):
        result.loc[i] = clear_data.loc[indexes[i]]

    return result
