# sorex_сryptotrade_bot
## Описание проекта:
sorex_сryptotrade_bot это телеграмм-бот отслеживающий min/max значения пар криптовалюта/USD в установленном диапазоне. Телеграмм бот умеет информировать пользователя о достижении пороговых значений, пороговые значения могут быть изменены по желанию пользователя через чат с ботом. Бот работает на удаленном сервере Ubuntu. Доступ к удаленному серверу возможен только по сетевому протоколу SSH. К серверу подключена система web-мониторинга ресурсов Cockpit.
#### Стек проекта: Python 3.11, Ubuntu, Cockpit
## Возможности проекта:
- Мониторинг курсов криптовалютных пар.
- Информирование о достижении min&max пороговых значений.
- Изменение пороговых значений криптовалютных пар.
- Мониторинг состояния ресурсов сервера.
- Информирование о критических нарушениях в работе сервера.
- Доступ к серверу по защищенному протоколу SSH.
## Установка и запуск проекта:
### Локально:
- Клонировать репозиторий:
  ```
  git clone git@github.com:aten88/sorex_сryptotrade_bot.git
  ```
- Установить и активировать виртуальное окружение:
  ```
  python -m venv venv
  ```
  ```
  source/venv/Scripts/activate
  ```
- Обновить пакетный менеджер pip:
  ```
  python.exe -m pip install --upgrade pip
  ```
- Установить зависимости из файла requirements.txt:
  ```
  pip install -r requirements.txt
  ```
- Создать файл с зависимостями .env в корне проекта и заполните его константами:
  ```
  YOUR_API_KEY=API-ключ вашего бота в ТГ.
  COIN_MARKET_API_KEY=API ключ платформы CoinMarketCap
  URL_MARKET = https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest
- Запустить скрипт:
  ```
  python bot.py
  ```

### На сервере:
- Обновить пакетный менеджер:
  ```
  sudo apt update
  ```
- Сгенерировать на сервере SSH-ключ для GitHub в терминале на сервере введите:
  ```
  ssh-keygen
  ```
  - Следуйте инструкциям запомните или сохраните учетные данные.

- Настроить подключение сервера к аккаунту на GitHub:
  - Выведете и скопируйте ключ ssh:
  ```
  cat .ssh/id_rsa.pub 
  ```
  - Добавьте ключ в настройки своего аккаунта на GitHub раздел SSH and GPG keys.
- Клонировать репозиторий:
  ```
  git clone git@github.com:aten88/sorex_сryptotrade_bot.git
  ```
- Перейдите в директорию с проектом:
  ```
  cd sorex_сryptotrade_bot
  ```
- Установить и активировать виртуальное окружение:
  ```
  sudo apt install python3-pip python3-venv -y
  ```
  ```
  source venv/bin/activate
  ```
- Обновить пакетный менеджер pip:
  ```
  pip install --upgrade pip
  ```
- Установить зависимости из файла requirements.txt:
  ```
  pip install -r requirements.txt 
  ```
- Создать файл с зависимостями .env в корне проекта и заполните его константами:
  ```
  YOUR_API_KEY=API-ключ вашего бота в ТГ.
  COIN_MARKET_API_KEY=API ключ платформы CoinMarketCap
  URL_MARKET = https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest
  ```
- Запустить скрипт:
  ```
  python3 bot.py
  ```
  - или с сохранением работы:
  ```
  nohup python3 bot.py &
  ```
  - Чтобы остановить процесс введите в терминале:
    ```
    ps aux | grep 'python3 bot.py'
    ```
    ```
    kill PID-номер операции
    ```

### Автор: Алексей Тен.
