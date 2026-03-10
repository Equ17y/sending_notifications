# Telegram-бот для уведомлений о проверке работ Devman

Бот следит за проверками работ на платформе [Devman](https://dvmn.org) и присылает уведомления в Telegram.

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Equ17y/dvmn-telegram-bot.git
cd dvmn-telegram-bot
```

### 2. Создайте виртуальное окружение

```bash
python -m venv myvenv
myvenv\Scripts\activate
```

### 3.Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте файл .env

```bash
DVMN_TOKEN=ваш_токен_от_Devman
TELEGRAM_TOKEN=ваш_токен_telegram_bot
TG_CHAT_ID=ваш_chat_id
```

### 5.Запустите бота

```bash
python bot.py
```