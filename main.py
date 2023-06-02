import telebot
import requests
from bs4 import BeautifulSoup

# Ваш API ключ от OpenWeatherMap
OPENWEATHERMAP_API_KEY = '13550893a41439cd63ac321594cb62a2'

# Создание экземпляра бота
bot = telebot.TeleBot('6162595567:AAE3rBdQvGrwnFqnHcsP_072ZNSUFb15IHk')

#Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я бот, который предоставляет информацию о погоде и курсах валют. Введите /weather для получения прогноза погоды или /currency для получения курса валют.')

# Обработчик команды /currency
@bot.message_handler(commands=['currency'])
def handle_currency_command(message):
    bot.reply_to(message, 'Введите название валюты для получения текущего курса.')

# Обработчик команды /weather
@bot.message_handler(commands=['weather'])
def handle_weather_command(message):
    bot.reply_to(message, 'Введите название города для получения прогноза погоды.')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        command = message.text[1:].strip().lower()
        if command == 'currency':
            bot.reply_to(message, 'Введите название валюты для получения текущего курса.')
        elif command == 'weather':
            bot.reply_to(message, 'Введите название города для получения прогноза погоды.')
        else:
            bot.reply_to(message, 'Команда не распознана. Введите /currency для получения курса валюты или /weather для получения прогноза погоды.')

    else:
        city = message.text.strip()
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
        response = requests.get(weather_url).json()
        if response.get('cod') == 200 and city != 'EUR':
            weather_description = response['weather'][0]['description']
            temperature = response['main']['temp']
            humidity = response['main']['humidity']
            wind_speed = response['wind']['speed']
            reply = f'Погода в городе {city}:\nОписание: {weather_description}\nТемпература: {temperature}°C\nВлажность: {humidity}%\nСкорость ветра: {wind_speed} м/с'
            bot.reply_to(message, reply)
        else:
            currency = message.text.strip().upper()
            if currency == 'RUB':
                bot.reply_to(message, 'Курс RUB к RUB: 1')
            else:
                url = f"https://www.google.com/search?q={currency}+to+RUB"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    rate_element = soup.find('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
                    rate = rate_element.text
                    bot.reply_to(message, f'Курс {currency} к RUB: {rate}')
                except (requests.RequestException, ValueError, AttributeError):
                    bot.reply_to(message, 'Не удалось получить информацию о курсе валюты.')

# Запуск бота
bot.polling()
