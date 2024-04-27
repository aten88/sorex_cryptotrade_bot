import os

import asyncio
import requests
import telebot
import threading
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, CoinValues
from constants import ROUNDER_VALUE

load_dotenv()

BOT_API_KEY = os.getenv('YOUR_API_KEY')
CHAT_ID = os.getenv('YOUR_CHAT_ID')
COIN_API_KEY = os.getenv('COIN_MARKET_API_KEY')
INTERVAL = os.getenv('INTERVAL_TIME')
DESCRIPTION = (
    'Этот бот 🤖 отслеживает значения пороговых сумм 🪙Криптовалюта/USD💲,'
    ' min 👇👆 max , при достижении или превышении, которых приходит сообщение'
    ' 📩 в чат. Для установки ⚙️ новых значений используйте команду /update.'
    'Чтобы просмотреть значения криптовалютных пар'
    ' и их min/max значений используйте команду /show'
)

bot = telebot.TeleBot(BOT_API_KEY)

engine = create_engine('sqlite:///coin_values.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def send_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)


def get_price(coin):
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


async def tracking_values(coin, min_price, max_price):
    while True:
        price = get_price(coin)
        if price <= min_price:
            send_message(
                f'Цена {coin}={price}$, '
                f'достигла или меньше порога: ${min_price}'
            )
        elif price >= max_price:
            send_message(
                f'Цена {coin}={price}$, '
                f'достигла или больше максимального порога: ${max_price}'
            )
        await asyncio.sleep(int(INTERVAL))


def polling_thread():
    bot.polling()


async def main():
    coin_values = session.query(CoinValues).all()

    tasks = []
    for coin_value in coin_values:
        task = asyncio.create_task(
            tracking_values(
                coin_value.coin_name,
                coin_value.min_price,
                coin_value.max_price,
            )
        )
        tasks.append(task)
    await asyncio.gather(*tasks)


@bot.message_handler(commands=['update'])
def update_message(message):
    bot.send_message(
        chat_id=CHAT_ID,
        text='Введите название криптовалюты и новые значения в формате: '
        'Тикер, min, max'
    )


@bot.message_handler(commands=['show'])
def show_message(message):
    coin_values = session.query(CoinValues).all()
    if coin_values:
        message = "Текущие значения криптовалют:\n"
        for coin_value in coin_values:
            message += (
                f"{coin_value.coin_name}: min - "
                f"{coin_value.min_price}$, max - {coin_value.max_price}$\n"
            )
    else:
        message = "Нет сохраненных значений криптовалют."
    bot.send_message(chat_id=CHAT_ID, text=message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/') and message.text != '/update':
        bot.send_message(
            chat_id=CHAT_ID,
            text='Неизвестная команда. Для обновления значений '
            'используйте команду /update'
        )
    else:
        try:
            coin, min_price, max_price = message.text.split(',')
            coin = coin.strip().upper()
            min_price = float(min_price.strip())
            max_price = float(max_price.strip())

            existing_coin = session.query(
                CoinValues).filter_by(coin_name=coin).first()
            if existing_coin:
                existing_coin.min_price = min_price
                existing_coin.max_price = max_price
            else:
                new_coin = CoinValues(
                    coin_name=coin, min_price=min_price,
                    max_price=max_price, user_id=CHAT_ID
                )
                session.add(new_coin)
            session.commit()
            bot.send_message(
                chat_id=CHAT_ID, text='Значения успешно обновлены.'
            )

        except Exception:
            bot.send_message(
                chat_id=CHAT_ID, text='Ошибка при обновлении значений. '
                'Пожалуйста, введите криптовалюту и новые значения в '
                'правильном формате.'
            )


if __name__ == '__main__':
    send_message(DESCRIPTION)
    polling_thread = threading.Thread(target=polling_thread)
    polling_thread.start()
    asyncio.run(main())
    polling_thread.join()
