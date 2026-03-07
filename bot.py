import requests
import time
import os
from dotenv import load_dotenv
from requests.exceptions import ReadTimeout, ConnectionError

load_dotenv()

TOKEN = os.getenv('TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

url = 'https://dvmn.org/api/long_polling/'
telegram_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

headers = {'Authorization': f'Token {TOKEN}'}

timestamp = time.time()  # Начинаем с текущего времени


def send_notification(text):
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(telegram_url, data=data)

while True:
    params = {'timestamp': timestamp}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'found':
            for attempt in data['new_attempts']:
                title = attempt['lesson_title']
                is_negative = attempt['is_negative']
                lesson_url = attempt.get('lesson_url', 'https://dvmn.org')
                
                # Формируем сообщение по заданию
                if is_negative:
                    message = (
                        f'У вас проверили работу "{title}"\n\n'
                        f'К сожалению, в работе нашлись ошибки'
                    )
                else:
                    message = (
                        f'У вас проверили работу "{title}"\n\n'
                        f'Преподавателю все понравилось, можно приступать к следующему уроку!'
                    )
                
                #  Добавляем ссылку на урок (опционально, как в задании)
                message += f'\n\n{lesson_url}'
                
                send_notification(message)
        
        # Обновляем timestamp из ответа сервера
        timestamp = data.get('last_attempt_timestamp') or data.get('timestamp_to_request') or time.time()
        
    except ReadTimeout:
        # Сервер не ответил за 5 секунд — повторяем запрос
        pass
    
    except ConnectionError:
        # Нет соединения с интернетом — ждём и повторяем запрос
        pass

