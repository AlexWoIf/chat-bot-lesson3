import logging
import os
import telegram

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

from dialog_flow import detect_intent_text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def reply(update, context):
    logger.debug(f'Enter reply {update.message.text=}')
    text = update.message.text
    session = update.effective_chat.id
    answer = detect_intent_text(project_id, session, text, 'ru')
    update.message.reply_text(answer.fulfillment_text)


def main():
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
    loglevel = os.getenv('LOG_LEVEL', default='INFO')
    log_chat = os.getenv('LOG_TG_CHAT_ID')
    log_tg_token = os.getenv('LOG_TG_BOT_TOKEN')
    logger.setLevel(loglevel)
    if log_chat:
        if not log_tg_token:
            log_tg_token = tg_token
        logger.addHandler(TelegramLogsHandler(log_tg_token, log_chat))
    logger.info('Start logging')

    try:
        main()
    except Exception as error:
        logger.error(error)
