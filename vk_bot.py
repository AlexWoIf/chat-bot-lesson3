import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialog_flow import detect_intent_texts


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def echo(event, vk_api):
    text = event.text
    session = event.user_id
    answer = detect_intent_texts(project_id, session, text, 'ru')

    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('VK_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

    vk_session = vk.VkApi(token=api_key)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
                echo(event, vk_api)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)
