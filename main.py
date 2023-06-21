import logging
import os
import requests
import telegram
from dotenv import load_dotenv
from time import sleep


def main():
    load_dotenv()
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    DEVMAN_TOKEN = os.getenv("DEVMAN_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")
    bot = telegram.Bot(token=TG_BOT_TOKEN)
    url = 'https://dvmn.org/api/long_polling/'
    payload = {}
    headers = {
        'Authorization': f'Token {DEVMAN_TOKEN}'
    }

    while True:
        try:
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
            logging.info('Бот запущен')
            reviews = response.json()

            if reviews['status'] == 'timeout':
                payload = {
                    'timestamp': reviews['timestamp_to_request']
                }
            if reviews['status'] == 'found':
                payload = {
                    'timestamp': reviews['last_attempt_timestamp']
                }
                for attempt in reviews['new_attempts']:
                    lesson_title = attempt['lesson_title']
                    is_negative = attempt['is_negative']
                    lesson_url = attempt['lesson_url']
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
        except requests.exceptions.ReadTimeout:
            logging.error('Нет подключения к серверу')
            continue
        except requests.exceptions.ConnectionError:
            logging.error('Ошибка подключения к серверу')
            sleep(30)


if __name__ == '__main__':
    main()
