import telebot
from datetime import datetime
import pytz
import schedule
import time
import threading
from flask import Flask, request, jsonify

TOKEN = "7542022559:AAFpP7-ZId3x0aFon8OGGlTcnzNeZ1Jp42s"
bot = telebot.TeleBot(TOKEN)

schedule_data = {
    'Monday': {
        'numerator': {
           'group1': "1. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n2. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n3. Лекц. Веб-диз. та граф. диз. Електротехн.\n4. Вікно\n5. Лаб. Комп'ютерна логіка 1-208\n6. Лаб. Комп'ютерна логіка 1-208",
           'group2': "1. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n2. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n3. Вікно\n4. Лекц. Структури даних і алгоритми 1-107\n5. Лаб. Комп'ютерна логіка 1-208\n6. Лаб. Комп'ютерна логіка 1-208",
        },
        'denominator': {
           'group1': "1. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n2. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n3. Лекц. Веб-диз. та граф. диз. Електротехн.\n4. Вікно\n5. Лаб. Комп'ютерна логіка 1-208\n6. Лаб. Комп'ютерна логіка 1-208",
           'group2': "1. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n2. Лаб. Об'єктно-Орієнтоване Програмування 1-116\n3. Вікно\n4. Лекц. Структури даних і алгоритми 1-107\n5. Лаб. Комп'ютерна логіка 1-208\n6. Лаб. Комп'ютерна логіка 1-208",
        }
    },
    'Tuesday': {
        'numerator': {
            'group1': "3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ",
            'group2': "3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ\n5. Пр. Структури даних і алгоритми 1-101\n6. Пр. Структури даних і алгоритми 1-101",
        },
        'denominator': {
            'group1': "3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ",
            'group2': "3. Лекц. Комп'ютерна логіка ТКМ\n4. Лекц. Теор. електр. та маг. кіл. ТКМ\n5. Лаб. Структури даних і алгоритми 1-208\n6. Лаб. Структури даних і алгоритми 1-208",
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
    message = f"Розклад на {day} ({week_type}):\n\n"
    
    if week_type in day_schedule:
        if 'group1' in day_schedule[week_type]:
            message += f"Підгрупа 1:\n{day_schedule[week_type]['group1']}\n"
        if 'group2' in day_schedule[week_type]:
            message += f"\nПідгрупа 2:\n{day_schedule[week_type]['group2']}\n"
    else:
        message = "Сьогодні немає занять."

    return message

def generate_full_schedule_message():
    timezone = pytz.timezone("Europe/Kiev")
    today = datetime.now(timezone).strftime('%A')
    week_type = 'numerator' if is_numerator_week() else 'denominator'

    message = f"Розклад на тиждень ({week_type}):\n\n"
    for day, schedule_for_day in schedule_data.items():
        if day == today:
            message += f"{day} (Today):\n"
        else:
            message += f"{day}:\n"
        
        if week_type in schedule_for_day:
            if 'group1' in schedule_for_day[week_type]:
                message += f"  Підгрупа 1: {schedule_for_day[week_type]['group1']}\n"
            if 'group2' in schedule_for_day[week_type]:
                message += f"  Підгрупа 2: {schedule_for_day[week_type]['group2']}\n"
        message += "\n"
    
    return message

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я бот, який допоможе тобі зі шкільним розкладом.")

@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, "Hello World!")

@bot.message_handler(commands=['today'])
def today(message):
    timezone = pytz.timezone("Europe/Kiev")
    today = datetime.now(timezone).strftime('%A')
    bot.send_message(message.chat.id, generate_schedule_message(today))

@bot.message_handler(commands=['week'])
def week(message):
    bot.send_message(message.chat.id, generate_full_schedule_message())

def run_bot():
    bot.polling(none_stop=True)

def schedule_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Flask server для фіктивного веб-сервісу
app = Flask(__name__)

@app.route('/schedule', methods=['GET'])
def get_schedule():
    fake_schedule = {
        "Monday": "Math, Physics",
        "Tuesday": "Programming, Chemistry",
        "Wednesday": "Literature, History",
        "Thursday": "PE, Biology",
        "Friday": "Math, Art"
    }
    return jsonify(fake_schedule)

@app.route('/schedule', methods=['POST'])
def post_schedule():
    data = request.json
    return jsonify({"status": "Schedule received", "data": data}), 201

def run_flask():
    app.run(debug=True, port=5000)

# Запуск бота та Flask серверу у різних потоках
if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    flask_thread = threading.Thread(target=run_flask)

    bot_thread.start()
    flask_thread.start()
