import time
import datetime
import requests
from fuzzywuzzy import fuzz

from init_bot import bot
from translations import translate


def _(text, lang='ru'):
    """Перевод текста"""
    if lang == 'ru':
        return text
    else:
        global translate
        try:
            return translate[lang][text]
        except:
            return text


def days_to_seconds(days):
    """"Перевод дней в секунды"""
    return days * 86400

def time_sub_day(get_time):
    """"Кол-во дней до окончания подписки"""
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        return str(datetime.timedelta(seconds=middle_time)).replace('days', 'дней').replace('day', 'день')
    

def recognize_question(question, questions):
    """"Распознавание вопроса"""
    recognized = {'id': '', 'percent': 0}
    for key, value in questions.items():
        for q in value:
            percent = fuzz.ratio(question, q)
            if percent > recognized['percent']:
                recognized['id'] = key
                recognized['percent'] = percent
    return recognized['id']


def get_rate():
    """"Получение курса валют"""
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    return round(response.json()['Valute']['USD']['Value'], 2)


async def check_sub_channels(channels, user_id):
    """Проверка подписки на несколько каналов"""
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member.status == 'left':
            return False
    return True



    








