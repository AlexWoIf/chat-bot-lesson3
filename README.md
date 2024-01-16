# Боты для Телеграм и ВК с использованием [Dialogflow](https://cloud.google.com/dialogflow?hl=ru)
Google сервис Dialogflow позволяет определять тематику сообщения и предлагает подходящий ответ.

## Подготовка к запуску, настройка окружения

Для запуска Вам понадобится установленный Python версии 3.10

Скачайте код с GitHub. Затем установите зависимости командой

```sh
pip install -r requirements.txt
```

## Подготовка проекта/настройка параметров

- Создайте группу вконтакте для получения токена -> [vk API](https://vk.com/dev/bots_docs).
- Выполните описанные условия для создания Google проекта [google cloud](https://cloud.google.com/dialogflow/docs/quick/api) и создайте [dialogflow agent](https://cloud.google.com/dialogflow/docs/quick/api).
- Получите все токены/ключи для заполнения `.env` файла.

```.env
TG_BOT_TOKEN=<получите у [**BotFather**](https://telegram.me/BotFather)>
GOOGLE_CLOUD_PROJECT=<ID проекта от [Google](console.cloud.google.com)>
GOOGLE_APPLICATION_CREDENTIALS=<путь до файла key.json с GOOGLE_APPLICATION_CREDENTIALS>
VK_API_KEY=<получите в интерфейсе настроек группы ВК>
LOG_LEVEL=[NOTSET|DEBUG|(INFO)|WARN|ERROR|CRITICAL] необязательный параметр. По умолчанию - INFO.
LOG_TG_CHAT_ID=<ID для отправки логов, можете узнать у [**userinfobot**](https://telegram.me/userinfobot)>
LOG_TG_BOT_TOKEN=<токен бота для отправки логов. можете не указывать, если хотите использовать одного и того же ТГ-бота>
```

Так же не забудьте перед запуском добавить себе в контакт-лист созданного Вами телеграм-бота(ов) и отправьте ему любое сообщение.

## Запуск

Для запуска телеграм бота используйте следующую команду:

```sh
python telegram_bot.py
```

Пример работы бота:

![Телеграм](https://dvmn.org/filer/canonical/1569214094/323/)

Для запуска вконтакте бота используйте следующую команду:

```sh
python vk_bot.py
```

Пример работы бота:

![ВК](https://dvmn.org/filer/canonical/1569214089/322/)


## Обучение бота

Для обучения dialogflow агента предусмотрен скрипт `training.py`. В качестве исходных данных берется `question.json` из текущего каталога.
Для запуска выполните команду:

```sh
python train_intent.py
```

Пример json файла:

```json
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },  ...
```

## Цели проекта

Код написан в учебных целях — это урок в рамках курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).
