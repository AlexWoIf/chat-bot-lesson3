import os
import logging

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

from dialog_flow import detect_intent_texts

logger = logging.getLogger(__name__)
def echo(update, context):
    text = update.message.text
    session = update.effective_chat.id
    answer = detect_intent_texts(project_id, session, text, 'ru')
    update.message.reply_text(answer)


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()
