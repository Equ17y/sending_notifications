import os
import time
import requests
from dotenv import load_dotenv
from requests.exceptions import ReadTimeout, ConnectionError


DVMN_API_URL = 'https://dvmn.org/api/long_polling/'
TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/sendMessage'


def send_notification(text, chat_id, telegram_token):
    url = TELEGRAM_API_URL.format(token=telegram_token)
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)
    
    
def get_dvmn_checks(timestamp, dvmn_token):
    headers = {'Authorization': f'Token {dvmn_token}'}
    params = {'timestamp': timestamp}
    response = requests.get(DVMN_API_URL, headers=headers, params=params, timeout=5)
    response.raise_for_status()
    return response.json()


def format_check_message(attempt):
    title = attempt['lesson_title']
    is_negative = attempt['is_negative']
    lesson_url = attempt.get('lesson_url', 'https://dvmn.org')
    
    if is_negative:
        text = (
            f'У вас проверили работу "{title}"\n\n'
            f'К сожалению, в работе нашлись ошибки '
        )
    else:
        text = (
            f'У вас проверили работу "{title}"\n\n'
            f'Преподавателю все понравилось, можно приступать к следующему уроку!'
        )
    
    text += f'\n\n{lesson_url}'
    return text


def main():
    load_dotenv()

    dvmn_token = os.environ['DVMN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    
    timestamp = time.time()
    
    while True:
        params = {'timestamp': timestamp}
        
        try:
            checks_response = get_dvmn_checks(timestamp, dvmn_token)
            
            if checks_response.get('status') == 'found':
                for attempt in checks_response['new_attempts']:
                    message = format_check_message(attempt)
                    send_notification(message, tg_chat_id, telegram_token)
                    
            timestamp = (
                checks_response.get('last_attempt_timestamp')
                or checks_response.get('timestamp_to_request')
                or time.time()
            )
            
        except ReadTimeout:
            pass
        
        except ConnectionError:
            time.sleep(10)
        
        
if __name__ == '__main__':
    main()  