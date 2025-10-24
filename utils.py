import datetime
import time


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