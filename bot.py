import os
import time

import asyncio
import requests
import telebot
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
    'Этот бот 🤖 отслеживает значения пороговых значений 🪙Криптовалюта/USD💲,'
    ' min 👇👆 max , при достижении или превышении, которых приходит сообщение'
    ' 📩 в чат. Для установки ⚙️ новых значений используйте команду /update'
)

bot = telebot.TeleBot(BOT_API_KEY)

engine = create_engine('sqlite:///coin_values.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def send_message(message):
    ''' Метод отправки сообщения в чат. '''
    bot.send_message(chat_id=CHAT_ID, text=message)


def get_price(coin):
    ''' Метод получения цены криптовалюты. '''
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
    ''' Метод отслеживания пороговых значений. '''
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


# def is_valid_coin(coin):
#     ''' Метод проверки существования криптовалюты. '''
#     url = 'https://api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#     response = requests.get(url)
#     data = response.json()
#     available_coins = [entry['symbol'].upper() for entry in data]
#     return coin.upper() in available_coins

send_message(DESCRIPTION)
time.sleep(int(INTERVAL))


async def main():
    ''' Основной метод. '''
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

if __name__ == '__main__':
    asyncio.run(main())
