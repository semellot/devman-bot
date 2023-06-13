# devman-bot

Бот для отправки уведомлений о проверке работ на курсах Devman.

## Как установить

Должен быть установлен Python3.
Затем используя pip установите зависимости:

```
pip install -r requirements.txt
```

Необходимо создать telegram-бот перед использованием.
Напишите Отцу ботов https://t.me/BotFather

Отец ботов попросит дать вашему боту два имени.
Первое — для отображения в списке контактов, может быть на русском.
Второе — служебное, по нему бота можно будет найти в поиске.
Должно быть на английском и заканчиваться на bot (например, notification_bot)

Создайте в каталоге проекта файл с названием `.env` со следующим наполнением:
```
TG_BOT_TOKEN=*** (токен, который дал Отец ботов для доступа к HTTP API)
TG_CHAT_ID=*** (ID пользователя Telegram)
DEVMAN_TOKEN=*** (персональный токен Devman)
```

## Пример запуска скрипта
```
% python main.py
```
