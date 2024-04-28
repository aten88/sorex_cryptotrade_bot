import os

import requests
import telebot
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, CoinValues
from constants import ROUNDER_VALUE

load_dotenv()

BOT_API_KEY = os.getenv('YOUR_API_KEY')
COIN_API_KEY = os.getenv('COIN_MARKET_API_KEY')
INTERVAL = os.getenv('INTERVAL_TIME')
DESCRIPTION = (
    'Этот бот 🤖 отслеживает значения пороговых сумм 🪙Криптовалюта/USD💲,'
    ' min 👇👆 max , при достижении или превышении, '
    ' которых приходит сообщение 📩 в чат. '
    ' Чтобы просмотреть значения криптовалютных пар'
    ' и их min/max значений используйте команду /show'
    ' Для установки ⚙️ новых значений используйте команду /update.'
    ' Для получения сводки котировок online используйте команду /tracking'
    ' Для повторного запуска бота введите команду /start'
)

bot = telebot.TeleBot(BOT_API_KEY)

engine = create_engine('sqlite:///coin_values.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_price(coin):
    ''' Метод получения котировки криптовалюты. '''
    url = os.getenv('URL_MARKET')
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COIN_API_KEY
    }
    parameters = {
        'symbol': coin,
        'convert': 'USD'
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    return round(data['data'][coin]['quote']['USD']['price'], ROUNDER_VALUE)


def tracking_values(user_id):
    ''' Метод отслеживания изменений котировок. '''
    coin_values = session.query(CoinValues).filter_by(user_id=user_id).all()
    any_coin_in_range = False
    for coin_value in coin_values:
        coin = coin_value.coin_name
        min_price = coin_value.min_price
        max_price = coin_value.max_price
        price = get_price(coin)
        if price <= min_price:
            bot.send_message(
                chat_id=user_id,
                text=f'Цена {coin}={price}$, '
                f'достигла или меньше порога: ${min_price}'
            )
            any_coin_in_range = True
        elif price >= max_price:
            bot.send_message(
                chat_id=user_id,
                text=f'Цена {coin}={price}$, '
                f'достигла или больше максимального порога: ${max_price}'
            )
            any_coin_in_range = True

    if not any_coin_in_range:
        bot.send_message(
            chat_id=user_id,
            text='Нет котировок соответствующих выбранным критериям.'
        )


@bot.message_handler(commands=['start'])
def start_message(message):
    ''' Обработчик команды /start'''
    bot.send_message(chat_id=message.chat.id, text=DESCRIPTION)


@bot.message_handler(commands=['update'])
def update_message(message):
    ''' Обработчик команды /update'''
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите название криптовалюты и новые значения в формате: '
        'Тикер, min, max'
    )


@bot.message_handler(commands=['show'])
def show_message(message):
    ''' Обработчик команды /show '''
    user_id = message.chat.id
    coin_values = session.query(CoinValues).filter_by(
        user_id=user_id
    ).all()
    if coin_values:
        answer = "Текущие значения криптовалют:\n"
        for coin_value in coin_values:
            answer += (
                f"{coin_value.coin_name}: min - "
                f"{coin_value.min_price}$, max - {coin_value.max_price}$\n"
            )
    else:
        answer = "Нет сохраненных значений криптовалют."
    bot.send_message(chat_id=message.chat.id, text=answer)


@bot.message_handler(commands=['tracking'])
def tracking_message(message):
    ''' Обработчик команды /tracking'''
    user_id = message.chat.id
    tracking_values(user_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    ''' Обработчик событий команд.'''
    if message.text.startswith('/') and message.text != '/update':
        bot.send_message(
            chat_id=message.chat.id,
            text='Неизвестная команда. Для обновления значений '
            'используйте команду /update'
        )
    else:
        try:
            coin, min_price, max_price = message.text.split(',')
            coin = coin.strip().upper()
            min_price = float(min_price.strip())
            max_price = float(max_price.strip())
            user_id = message.chat.id
            existing_coin = session.query(
                CoinValues).filter_by(
                    coin_name=coin,
                    user_id=user_id
                ).first()
            if existing_coin:
                existing_coin.min_price = min_price
                existing_coin.max_price = max_price
                existing_coin.user_id = user_id
            else:
                new_coin = CoinValues(
                    coin_name=coin, min_price=min_price,
                    max_price=max_price, user_id=user_id
                )
                session.add(new_coin)
            session.commit()
            bot.send_message(
                chat_id=user_id, text='Значения успешно обновлены.'
            )

        except Exception:
            bot.send_message(
                chat_id=message.chat.id, text='Ошибка при обновлении значений.'
                ' Пожалуйста, введите криптовалюту и новые значения в'
                ' формате: Тикер, min, max.'
            )


if __name__ == '__main__':
    bot.polling()
