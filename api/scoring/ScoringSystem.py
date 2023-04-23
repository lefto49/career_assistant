import numpy as np
import pandas as pd
import json
import re
import string
from nltk.stem import WordNetLemmatizer
import Levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.spatial as sp
import nltk
from pymorphy2 import MorphAnalyzer

from api.data.Vacancy import Vacancy

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def set_career_objective_by_experience(user, experience_df):
    user_experiennce = experience_df[experience_df['User ID'] == user['ID']]
    if len(user_experiennce) != 0:
        user_experiennce = user_experiennce.sort_values(by=['Дата изм.'], ascending=False).iloc[0]
        return user_experiennce['Сфера деятельности']
    return np.NAN


def word_lemma(word, analyzer_ru, analyzer_en):
    if ord(word[0]) < 123:
        return analyzer_en.lemmatize(word)
    else:
        return analyzer_ru.parse(word)[0].normal_form


def preprocess_text(text, stop_words, analyzer_ru, analyzer_en):
    regex = re.compile('[%s]' % re.escape(string.punctuation + string.digits))
    text = regex.sub(' ', text)
    text = text.lower().split()
    text = [word_lemma(word, analyzer_ru, analyzer_en) for word in text]
    text = [word for word in text if word not in stop_words]
    return ' '.join(text)


def form_users_text(user_id, current_text, additional_text, columns, stop_words, analyzer_ru, analyzer_en):
    add_text = additional_text[additional_text['User ID'] == user_id][columns].values
    if not pd.isnull(add_text).any():
        add_text = preprocess_text(' '.join(add_text), stop_words, analyzer_ru, analyzer_en)
        return current_text + ' ' + add_text
    else:
        return current_text


def set_vacancy_by_career_objective(user, jobs):
    res = []
    desire_words = user["Желаемая позиция"].split()

    for name, id in jobs[["title_edited", "id"]].values:
        job_words = name.split()
        similarity = []

        for jword in job_words:
            for eword in desire_words:
                similarity.append(1 - Levenshtein.distance(jword, eword) / max(len(jword), len(eword)))

        sort_sim = sorted(similarity, reverse=True)[:min(len(job_words), len(desire_words))]
        avg_sim = sum(sort_sim) / len(sort_sim)
        res.append((avg_sim, id))

    sim_sorted = sorted(res, key=lambda x: x[0], reverse=True)
    previous = sim_sorted[0][0]
    n = 0
    for pair in sim_sorted:
        if pair[0] == previous:
            n += 1
        elif n > 15:
            sim_sorted = sim_sorted[:n]
            break
        else:
            sim_sorted = sim_sorted[:15]
            break

    return ' '.join(map(str, list(zip(*sim_sorted))[1]))


def get_random_vacancy(jobs):
    indexes = np.random.randint(len(jobs), size=3)
    return jobs.iloc[indexes]['id'].values


def set_correlation_score_for_vacancies(user_df, vacancies_df):
    user_suggestion_df = vacancies_df.loc[map(int, user_df['Suggestion'].split())]
    user_suggestion_df = user_suggestion_df[user_suggestion_df['TF_IDF_VEC'].notna()]
    cosine_distances = 1 - sp.distance.cdist(np.array([user_df['TF_IDF_VEC']]),
                                             np.array(list(map(list, user_suggestion_df['TF_IDF_VEC'].to_numpy()))),
                                             'cosine')
    cosine_distances = np.nan_to_num(cosine_distances)
    return np.max(cosine_distances[0])


def load_data(experience, vacancy):
    vacancies = pd.DataFrame.from_records(Vacancy.objects.all().values())
    pymorphy2_analyzer_ru = MorphAnalyzer()
    analyzer_en = WordNetLemmatizer()
    with open('api/scoring/stopwords-ru.json', 'r') as openfile:
        stop_words = json.load(openfile)

    vacancy = preprocess_text(vacancy, stop_words, pymorphy2_analyzer_ru, analyzer_en)

    users = pd.DataFrame({
        'Желаемая позиция': [vacancy],
        'Text': [experience]
    }, index=[0])

    users_career = ~users['Желаемая позиция'].isnull()
    users_career = np.logical_and(users_career, users['Желаемая позиция'] != '')
    users.loc[~users['Желаемая позиция'].isnull(), 'Желаемая позиция'] = users[users_career]['Желаемая позиция'].apply(
        lambda obj: preprocess_text(obj, stop_words, pymorphy2_analyzer_ru, analyzer_en))
    users_texts = pd.DataFrame({
        'Желаемая позиция': [vacancy],
        'Text': [experience],
        'Suggestion': np.zeros(len(users)),
        'Correlation_score': np.zeros(len(users)),
        'TF_IDF_VEC': np.zeros(len(users))
    }, index=[0])
    # vacancies = vacancies[vacancies['description'].notna()]
    # vacancies['description'] = vacancies['description'].replace('_x000d_', ' ', regex=True)
    # vacancies['description'] = vacancies['description'].replace('_x000D_', ' ', regex=True)
    # vacancies['description'] = vacancies['description'].replace("\n", ' ', regex=True)
    # vacancies['description'] = vacancies['description'].replace('\[(.*?)\]', '', regex=True)
    # vacancies['description'] = vacancies['description'].apply(lambda vacancy: ' '.join(vacancy.split()))
    # vacancies['description'] = vacancies.apply(
    #     lambda text: preprocess_text(text['description'], stop_words, pymorphy2_analyzer_ru, analyzer_en),
    #     axis=1)
    # vacancies['НазваниеПреобр'] = vacancies['title'].apply(
    #     lambda obj: preprocess_text(obj, stop_words, pymorphy2_analyzer_ru, analyzer_en))
    vacancies = vacancies[vacancies['description_edited'].notna()]
    return vacancies, users_texts, users


def create_vectorizer(vacancies):
    # non_zero_rows = users_texts[(users_texts['Text'] != '') & (users_texts['Желаемая позиция'] != '')]
    overall_texts = vacancies['description_edited'].values.tolist()
    tf_idf_vec = TfidfVectorizer()
    tf_idf_vec.fit(overall_texts)
    X = tf_idf_vec.transform(vacancies['description_edited'])
    X.toarray()
    vacancies_df = pd.DataFrame(X.toarray(), columns=tf_idf_vec.get_feature_names())
    vacancies['TF_IDF_VEC'] = vacancies_df.apply(lambda vacancy: vacancy.to_numpy(), axis=1)
    return tf_idf_vec


def process_users(experience, vacancy):
    vacancies, users_texts, users = load_data(experience, vacancy)
    tf_idf_vec = create_vectorizer(vacancies)
    X = tf_idf_vec.transform(users_texts['Text'])
    X.toarray()
    users_df = pd.DataFrame(X.toarray(), columns=tf_idf_vec.get_feature_names())
    users_career = ~users['Желаемая позиция'].isnull()
    users_career = np.logical_and(users_career, users['Желаемая позиция'] != '')
    users_texts.loc[~users['Желаемая позиция'].isnull(), 'Suggestion'] = users[users_career].apply(
        lambda object: set_vacancy_by_career_objective(object, vacancies), axis=1)
    users_texts['Suggestion'] = users_texts['Suggestion'].fillna(0)
    vacancies_with_id = vacancies.set_index(['id'])
    users_texts['TF_IDF_VEC'] = users_df.apply(lambda user: user.to_numpy(), axis=1)
    users_texts['Correlation_score'] = users_texts[users_texts['Suggestion'] != 0.0].apply(
        lambda user: set_correlation_score_for_vacancies(user, vacancies_with_id), axis=1)
    users_texts['Correlation_score'] = users_texts['Correlation_score'].fillna(0)
    return users_texts['Correlation_score'].iloc[0]
