from flask import Flask, request
import logging
import json
import random
import os

app = Flask(__name__)

sessionStorage = {}

logging.basicConfig(level=logging.INFO)


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response'][
            'text'] = 'Возможная проблема: низкий уровень интеллекта. Скорость речи понижена на треть: Меня зовут ' \
                      'Скиппи. '
        res['response'][
            'tts'] = '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/2ba32bde-f845-47dc-96a3' \
                     '-77ece3c9fee0.opus"> '
        sessionStorage[user_id] = {
            'first_name': None
        }
        return
    elif 'включи что-нибудь' in req['request']['original_utterance'].lower():
        res['response'][
            'tts'] = '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/f02c9bc2-5a31-426b-919b' \
                     '-695d4058793a.opus"> '
        res['response']['text'] = 'Cкрашиваю ваше ожидание приятной мелодией.'
    else:
        res['response']['text'] = 'Чумба, ты совсем ебнутый? Сходи к мозгоправу, попей колесики. Примечание для себя: ' \
                                  'грубовато, надо как-то перефразировать. '
        res['response'][
            'tts'] = '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/0b557e02-c5ba-488a-acea' \
                     '-4dd6ffc97df4.opus"> '


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
