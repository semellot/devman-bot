import logging
import os
import requests
import telegram
from dotenv import load_dotenv
from time import sleep


logger = logging.getLogger('Logger')

class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    DEVMAN_TOKEN = os.getenv("DEVMAN_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(TG_BOT_TOKEN, TG_CHAT_ID))
    bot = telegram.Bot(token=TG_BOT_TOKEN)
    logger.info('Бот запущен')
    url = 'https://dvmn.org/api/long_polling/'
    payload = {}
    headers = {
        'Authorization': f'Token {DEVMAN_TOKEN}'
    }

    while True:
        try:
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
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
            logger.warning('Нет подключения к серверу')
            continue
        except requests.exceptions.ConnectionError:
            logger.warning('Ошибка подключения к серверу')
            sleep(30)


if __name__ == '__main__':
    main()
