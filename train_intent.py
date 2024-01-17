import json
import os
import logging

from dotenv import load_dotenv
from google.cloud import dialogflow


logger = logging.getLogger(__file__)


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
                                                    text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    return response


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    source = os.getenv('SOURCE_FILE_PATH', default='./question.json')
    loglevel = os.getenv('LOG_LEVEL', default='INFO')
    print(loglevel)
    logger.setLevel(loglevel)
    print(logger.getEffectiveLevel())
    logger.info('Start logging')

    with open(source, 'r', encoding='UTF-8', ) as source_file:
        intents_json = source_file.read()
    intents = json.loads(intents_json)

    headers = {}
    for theme_id, (display_name, payload)  in enumerate(intents.items(), 1):
        print(f'[{theme_id}] {display_name}')
        headers[theme_id] = display_name
    print('Выберите номер тематики, которую хотите добавить боту, '
          'либо введите 0, чтобы добавить сразу все темы:')
    theme_id = int(input())
    if theme_id:
        themes = [headers[theme_id]]
    else:
        themes = headers.values()
    print(f'Вы выбрали тему(ы): {themes}')

    for theme in themes:
        payload = intents[theme]
        training_phrases_parts = payload['questions']
        message_texts = payload['answer']
        try:
            response = create_intent(project_id, theme,
                                    training_phrases_parts, [message_texts,])
        except Exception as e:
            logger.error(f'{e}')
            continue
