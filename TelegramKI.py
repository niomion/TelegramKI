import telebot
from datetime import datetime, timedelta
import pytz
import schedule
import time
import threading
from telebot.types import BotCommand

TOKEN = "7542022559:AAFpP7-ZId3x0aFon8OGGlTcnzNeZ1Jp42s"
bot = telebot.TeleBot(TOKEN)

commands = [
    BotCommand(command="/class", description="Дізнатись пари на сьогодні"),
    BotCommand(command="/schedule", description="Отримати повний розклад на тиждень")
]

bot.set_my_commands(commands)

schedule_data = {
    'Monday': {
        'numerator': {
           'group1': "1. Лаб. Комп'ютерна логіка 1-116\n2. Лаб. Комп'ютерна логіка 1-116\n3. Лекц. Веб-диз. та граф. диз. Електротехн.",
           'group2': "1. Лаб. Комп'ютерна логіка 1-116\n2. Лаб. Комп'ютерна логіка 1-116\n3. Вікно\n4. Лекц. Структури даних і алгоритми 1-107",
        },
        'denominator': {
         'group1': "1. Лаб. Комп'ютерна логіка 1-116\n2. Лаб. Комп'ютерна логіка 1-116\n3. Лекц. Веб-диз. та граф. диз. Електротехн.\n4. Вікно\n5. Лаб. Об'єктно-Орієнтоване Програмування 1-205\n6. Лаб. Об'єктно-Орієнтоване Програмування 1-205",
           'group2': "1. Лаб. Комп'ютерна логіка 1-116\n2. Лаб. Комп'ютерна логіка 1-116\n3. Вікно\n4. Лекц. Структури даних і алгоритми 1-107\n5. Лаб. Об'єктно-Орієнтоване Програмування 1-205\n6. Лаб. Об'єктно-Орієнтоване Програмування 1-205",
        }
    },
    'Tuesday': {
        'numerator': {
            'group1': "3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ",
            'group2': "3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ\n5. Пр. Структури даних і алгоритми 1-101\n6. Пр. Структури даних і алгоритми 1-101",
        },
        'denominator': {
            'group1': "1. Лаб. Об'єктно-Орієнтоване Програмування 1-205\n2. Лаб. Об'єктно-Орієнтоване Програмування 1-205\n3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ",
            'group2': "1. Лаб. Об'єктно-Орієнтоване Програмування 1-205\n2. Лаб. Об'єктно-Орієнтоване Програмування 1-205\n3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ\n5. Лаб. Структури даних і алгоритми 1-208\n6. Лаб. Структури даних і алгоритми 1-208",
        }
    },
    'Wednesday': {
        'numerator': {
           'group1': "1. Лекц. Об'єктно-орієнтоване програмування 2-204\n2. Пр. Англ. м. проф. спрям. 4-412\n3. Пр. Об'єктно-орієнтоване програмування 1-101",
           'group2': "1. Лекц. Об'єктно-орієнтоване програмування 2-204\n2. Пр. Англ. м. проф. спрям. 4-412\n3. Пр. Об'єктно-орієнтоване програмування 1-101",
        },
        'denominator': {
           'group1': "1. Лекц. Об'єктно-орієнтоване програмування 2-204\n2. Пр. Англ. м. проф. спрям. 4-412\n3. Пр. Об'єктно-орієнтоване програмування 1-101\n4. Лаб. Теор. електр. та маг. кіл. 4-318",
           'group2': "1. Лекц. Об'єктно-орієнтоване програмування 2-204\n2. Пр. Англ. м. проф. спрям. 4-412\n3. Пр. Об'єктно-орієнтоване програмування 1-101\n4. Лаб. Теор. електр. та маг. кіл. 4-318",
        }
    },
    'Thursday': {
        'numerator': {
          'group1': "4. Пр. Комп'ютетрна логіка 1-113\n5. Пр. Веб-диз. та граф. диз. 1-113\n6. Лаб. Веб-диз. та граф. диз. 1-206\n7. Лаб. Веб-диз. та граф. диз. 1-206",
          'group2': "4. Пр. Комп'ютетрна логіка 1-113",
        },
        'denominator': {
           'group1': "3. Пр. Теор. електр. та маг. кіл. 4-318\n4. Пр. Комп'ютетрна логіка 1-113\n5. Пр. Веб-диз. та граф. диз. 1-113",
           'group2': "3. Пр. Теор. електр. та маг. кіл. 4-318\n4. Пр. Комп'ютетрна логіка 1-113",
        }
    },
}

special_fridays = {
    '2024-09-06': 'Monday',
    '2024-09-13': 'Tuesday',
    '2024-09-20': 'Wednesday',
    '2024-09-27': 'Thursday',
    '2024-10-04': 'Monday',
    '2024-10-11': 'Tuesday',
    '2024-10-18': 'Wednesday',
    '2024-10-25': 'Thursday',
    '2024-11-01': 'Monday',
    '2024-11-08': 'Tuesday',
    '2024-11-15': 'Wednesday',
    '2024-11-22': 'Thursday',
}

def is_numerator_week():
    week_number = datetime.now().isocalendar()[1]
    return week_number % 2 == 0  

def get_friday_schedule(date_str):
    if date_str in special_fridays:
        return special_fridays[date_str]
    month = datetime.strptime(date_str, '%Y-%m-%d').strftime('%B')
    
    week_type = 'numerator'
    if month == 'October':
        week_type = 'denominator'
    elif month == 'November':
        week_type = 'numerator'
    
    return week_type


def generate_schedule_message(day):
    timezone = pytz.timezone("Europe/Kiev")
    today_str = datetime.now(timezone).strftime('%Y-%m-%d')

    if day == 'Friday':
        day = get_friday_schedule(today_str)
    
    day_schedule = schedule_data.get(day, {})
    
    if day == 'Saturday' or day == 'Sunday':
        return 'Сьогодні вихідний'

    week_type = 'numerator' if is_numerator_week() else 'denominator'
    week_typeukr = 'Чисельник' if week_type == 'numerator' else 'Знаменник'
    if day == 'Monday': dayukr = 'Понеділок'
    elif day == 'Tuesday': dayukr = 'Вівторок'
    elif day == 'Wednesday': dayukr = 'Середу'
    elif day == 'Thursday': dayukr = 'Четвер'
    elif day == 'Friday':dayukr = 'П’ятницю'
    elif day == 'Saturday': dayukr = 'Суботу'
    elif day == 'Sunday': dayukr = 'Неділю'

    message = f"💬 <b>Розклад на {dayukr} ({week_typeukr}):</b>\n\n"
    
    if week_type in day_schedule:
        if 'group1' in day_schedule[week_type]:
            message += f"📍<b>Підгрупа 1:</b>\n{day_schedule[week_type]['group1']}\n"
        if 'group2' in day_schedule[week_type]:
            message += f"\n📍<b>Підгрупа 2:</b>\n{day_schedule[week_type]['group2']}\n"
    else:
        message = "Сьогодні немає занять."

    return message

def generate_full_schedule_message():
    timezone = pytz.timezone("Europe/Kiev")
    week_type = 'numerator' if is_numerator_week() else 'denominator'
    week_typeukr = 'Чисельник' if week_type == 'numerator' else 'Знаменник'
    message = f"💬 <b>Розклад на тиждень ({week_typeukr}):</b>\n\n"
    for day, schedules in schedule_data.items():
        if day == 'Monday':
            dayukr = 'Понеділок'
        elif day == 'Tuesday':
            dayukr = 'Вівторок'
        elif day == 'Wednesday':
            dayukr = 'Середу'
        elif day == 'Thursday':
            dayukr = 'Четвер'
        elif day == 'Friday':
            dayukr = 'П’ятницю'
        elif day == 'Saturday':
            dayukr = 'Суботу'
        elif day == 'Sunday':
            dayukr = 'Неділю'
        if day == 'Friday':
            day = get_friday_schedule(datetime.now(timezone).strftime('%Y-%m-%d'))
        if week_type in schedules:
            message += f"<b>🗓 Розклад на {dayukr}:</b>\n\n"
            if 'group1' in schedules[week_type]:
                message += f"📍<b>Підгрупа 1:</b>\n{schedules[week_type]['group1']}\n"
            if 'group2' in schedules[week_type]:
                message += f"\n📍<b>Підгрупа 2:</b>\n{schedules[week_type]['group2']}\n"
            message += "\n"
    return message

def send_tomorrow_schedule():
    timezone = pytz.timezone("Europe/Kiev")
    tomorrow = (datetime.now(timezone) + timedelta(days=1)).strftime('%A')
    
    schedule_message = generate_schedule_message(tomorrow)
    
    chat_id = '-1001959771080'  # Замініть на ваш чат ID
    bot.send_message(chat_id, schedule_message, parse_mode='HTML')

def send_daily_schedule():
    timezone = pytz.timezone("Europe/Kiev")
    today = datetime.now(timezone).strftime('%A')
    
    schedule_message = generate_schedule_message(today)
    
    chat_id = '-1001959771080'
    bot.send_message(chat_id, schedule_message, parse_mode='HTML')

schedule.every().monday.at("03:00").do(send_daily_schedule)
schedule.every().tuesday.at("03:00").do(send_daily_schedule)
schedule.every().wednesday.at("03:00").do(send_daily_schedule)
schedule.every().thursday.at("03:00").do(send_daily_schedule)
schedule.every().friday.at("03:00").do(send_daily_schedule)
schedule.every().monday.at("17:00").do(send_tomorrow_schedule)
schedule.every().tuesday.at("17:00").do(send_tomorrow_schedule)
schedule.every().wednesday.at("17:00").do(send_tomorrow_schedule)
schedule.every().thursday.at("17:00").do(send_tomorrow_schedule)
schedule.every().sunday.at("17:00").do(send_tomorrow_schedule)
schedule.every().day.at("13:40").do(send_tomorrow_schedule)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

@bot.message_handler(commands=['class'])
def send_welcome(message):
    timezone = pytz.timezone("Europe/Kiev")
    current_time = datetime.now(timezone)
    today = current_time.strftime('%A')
    if current_time.hour < 20:
        schedule_message = generate_schedule_message(today)
    else:
        tomorrow = (current_time + timedelta(days=1)).strftime('%A')
        schedule_message = generate_schedule_message(tomorrow)
    
    bot.reply_to(message, schedule_message, parse_mode='HTML')

@bot.message_handler(commands=['schedule'])
def send_full_schedule(message):
    schedule_message = generate_full_schedule_message()
    bot.reply_to(message, schedule_message, parse_mode='HTML')

bot.polling()