from dotenv import load_dotenv
import os
import requests
import telegram


load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
DEVMAN_TOKEN = os.getenv("DEVMAN_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
bot = telegram.Bot(token=TG_BOT_TOKEN)
url = 'https://dvmn.org/api/long_polling/'

headers = {
    'Authorization': f'Token {DEVMAN_TOKEN}'
}
response = requests.get(url, headers=headers)
response.raise_for_status()
print(response.json())
timestamp_to_request = response.json()['new_attempts'][0]['timestamp']

def get_status(timestamp_to_request):
    try:
        while True:
            payload = {'timestamp': timestamp_to_request}
            response = requests.get(url, params=payload, headers=headers, timeout=190)
            response.raise_for_status()
            for message in response:
                print(response.json())
                if response.json()['status'] == 'timeout':
                    timestamp_to_request = response.json()['timestamp_to_request']
                elif response.json()['status'] == 'found':
                    lesson_title = response.json()['new_attempts'][0]['lesson_title']
                    is_negative = response.json()['new_attempts'][0]['is_negative']
                    lesson_url = response.json()['new_attempts'][0]['lesson_url']
                    if is_negative:
                        bot.send_message(
                            chat_id=TG_CHAT_ID,
                            text=f'''У вас проверили работу «{lesson_title}».

                            К сожалению в работе нашлись ошибки.
                            {lesson_url}
                            '''
                        )
                    else:
                        bot.send_message(
                            chat_id=TG_CHAT_ID,
                            text=f'''У вас проверили работу «{lesson_title}».

                            Преподавателю всё понравилось, можно приступать к следующему уроку!
                            {lesson_url}
                            '''
                        )
                    timestamp_to_request = response.json()['last_attempt_timestamp']
                print(timestamp_to_request)
    except requests.exceptions.ReadTimeout:
        print('ReadTimeout')
        get_status(timestamp_to_request)
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
        get_status(timestamp_to_request)

get_status(timestamp_to_request)
