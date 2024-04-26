# sorex_kryptotrade_bot
## Описание проекта:
sorex_kryptotrade_bot это телеграмм-бот отслеживающий min/max значения пар криптовалюта/USD в установленном диапазоне. Телеграмм бот умеет информировать пользователя о достижении пороговых значений, пороговые значения могут быть изменены по желанию пользователя через чат с ботом. Бот работает на удаленном сервере Ubuntu. Доступ к удаленному серверу возможен только по сетевому протоколу SSH. К серверу подключена система web-мониторинга ресурсов Cockpit.
#### Стек проекта: Python 3.11, Ubuntu, Cockpit
## Возможности проекта:
- Мониторинг курсов криптовалютных пар
- Информирование о достижении min&max пороговых значений
- Изменение пороговых значений криптовалютных пар
- Мониторинг состояния ресурсов сервера
- Информирование о критических нарушениях в работе сервера
- Доступ к серверу по защищенному протоколу SSH.
## Установка и запуск проекта:
### Локально:
- Клонировать репозиторий:
  ```
  git clone git@github.com:aten88/sorex_kryptotrade_bot.git
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
- Запустить скрипт:
  ```
  python name.py
  ```

### На сервере:

### Автор: Алексей Тен.
