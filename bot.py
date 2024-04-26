import os

import asyncio
import requests
import telebot
from dotenv import load_dotenv

from constants import ROUNDER_VALUE

load_dotenv()

BOT_API_KEY = os.getenv('YOUR_API_KEY')
CHAT_ID = os.getenv('YOUR_CHAT_ID')
COIN_API_KEY = os.getenv('COIN_MARKET_API_KEY')
INTERVAL = os.getenv('INTERVAL_TIME')

bot = telebot.TeleBot(BOT_API_KEY)


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


async def main():
    ''' Основной метод. '''
    coin_values = {
        'BTC': {'min': 63800, 'max': 64000},
        'ETH': {'min': 3200, 'max': 3500},
        'MKR': {'min': 2900, 'max': 3000},
    }

    tasks = []
    for coin, values in coin_values.items():
        min_price = values['min']
        max_price = values['max']
        task = asyncio.create_task(tracking_values(coin, min_price, max_price))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
