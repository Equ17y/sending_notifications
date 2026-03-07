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

timestamp = time.time()


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
                
                message += f'\n\n{lesson_url}'
                
                send_notification(message)

        timestamp = data.get('last_attempt_timestamp') or data.get('timestamp_to_request') or time.time()
        
    except ReadTimeout:
        pass
    
    except ConnectionError:
        pass

