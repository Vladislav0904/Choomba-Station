from flask import Flask, request
import logging
import json
import random
import os

app = Flask(__name__)

sessionStorage = {}
logging.basicConfig(level=logging.INFO)

facts = \
    {
        'Любопытный факт: Человеческое тело содержит от 5 до 7 литров крови.':
            '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/627eef66-548c-45ca-8790-48429fc08925'
            '.opus">',
        'Любопытный факт: После отрубания головы, мозг еще несколько минут сохраняет активность.':
            '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/6026210b-65bf-4e9a-a51a-0ff72febeffd'
            '.opus"> ',
        'Любопытный факт: Большинство убийств совершается мужчинами - такими, вроде тебя.':
            '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/95034303-2ce3-4dd1-b01a-cd11aa0e9883'
            '.opus"> ',
        'Любопытный факт хозяйке на заметку! Пятна крови можно легко удалить с помощью уксуса.':
            '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/2b79edb4-4553-4105-8fb0-a058cb25d911'
            '.opus"> ',
        'Любопытный факт: согласно традиционным христианским воззрениям, вы сгорите в аду.':
            '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/edab618a-c038-4562-94dd-e68847a18fa5'
            '.opus"> '
    }


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
    joke = False
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response'][
            'text'] = 'Добро пожаловать в Чумба.Станцию. Ваш новый помощник Скиппи умеет рассказывать некоторые ' \
                      'факты, играть свою музыку, а также немного общаться с вами. '
        sessionStorage[user_id] = {
            'first_name': None
        }
        return
    elif 'тебя зовут' in req['request']['original_utterance'].lower():
        res['response'][
            'text'] = 'Возможная проблема: низкий уровень интеллекта. Скорость речи понижена на треть: Меня зовут ' \
                      'Скиппи. '
        res['response'][
            'tts'] = '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/2ba32bde-f845-47dc-96a3' \
                     '-77ece3c9fee0.opus"> '
    elif 'помощь' in req['request']['original_utterance'].lower() or 'что ты умеешь' in req['request'][
        'original_utterance'].lower():
        res['response'][
            'text'] = 'Скиппи может рассказать вам интересные факты "расскажи факт", играть музыку "включи ' \
                      'что-нибудь" и немного общаться с вами '
    elif 'включи что-нибудь' in req['request']['original_utterance'].lower() or 'музык' in req['request'][
        'original_utterance'].lower() \
            or 'сыграй' in req['request']['original_utterance'].lower():
        res['response'][
            'tts'] = '<speaker audio="dialogs-upload/f0b2392a-f08b-404f-af1a-c0109eab8a69/f02c9bc2-5a31-426b-919b' \
                     '-695d4058793a.opus"> '
        res['response']['text'] = 'Cкрашиваю ваше ожидание приятной мелодией.'

    elif 'факт' in req['request']['original_utterance'].lower():
        name = random.choice(list(facts.keys()))
        res['response']['text'] = name
        res['response']['tts'] = facts.get(name)
    elif 'расскажи что-нибудь' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Приветствую Пользователь! Я подготовил для вас статистику. Скажите что-нибудь для ' \
                                  'продолжения. '
        joke = True
    elif 'что-нибудь' in req['request']['original_utterance'].lower() and joke:
        res['response'][
            'text'] = 'Кажется, вы пытались пошутить. Автоматический ответ: ха-ха-ха. Впервые слышу эту шутку.'
        joke = False
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
