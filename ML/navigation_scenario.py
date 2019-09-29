from ml_utils import *
from dialogue import *
from path_finder.path import find_path
import numpy as np

import traceback


class NavigationScenario(BaseScenario):
    # SCENARIO_ID=0
    def __init__(self):
        pass
    
    def answer(self, state, models):
        text = state['history_user'][-1]
        # RETURNS
        try:
            if state['return_to_id'] == 0:
                state['return_to_id'] = -1
                if state['return_message'] == 'where' or state['return_message'] == 'where_want':
                    if state['return_message'] == 'where':
                        state['return_message'] = ''
                        back_id = -2
                    elif state['return_message'] == 'where_want':
                        state['return_message'] = ''
                        back_id = -3

                    print("NavigationScenario back_id =", back_id)
                    text = state['history_user'][back_id] # Старый текст, куда хочет юзер
                    print("HistoryUser at back_id:", text)
                    tokens, ners = models['ner_model']([text])
                    tokens = np.array(tokens[0])
                    ners = np.array(ners[0])
                    mask = ners != 'O'
                    lemmatize_text = lemmatize(text.lower())
                    text_lemm_set = set(lemmatize_text.split())
                    for i, cl in enumerate(ners):
                        if 'ORG' in cl:
                            mask[i] = False
                    # a list of objects matching the given query, without elastic-specific fields
                    search_queue = ['objects', ['name', 'authors'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                    print('Search queue: {}'.format(str(search_queue)))
                    search_result = models['search'](*search_queue)
                    best_search = search_result[0]
                    print('Search result: {}'.format(best_search))
                    hall_to = best_search['hall']
                    building = best_search['building']
                    state['history_object'] = best_search
                    if building == '117':
                        buld = 'gallery'
                    else:
                        buld = 'main'

                    new_text = state['history_user'][-1] # Откуда идет юзер
                    hall_from = int(''.join(list(filter(str.isdigit, new_text.lower()))))
                    path = models['find_path'](buld, str(hall_from), str(hall_to))
                    result_text = []
                    for item in path[1:]:
                        if item['type'] == 'hall':
                            result_text.append('Пройдите в зал ' + str(item['index']))
                        else:
                            if item['direction'] == 'up':
                                result_text.append('Поднимитесь по лестнице')
                            else:
                                result_text.append('Спуститесь по лестнице')
                    result_text = '. '.join(result_text) + '.'
                    result = {}
                    result['text'] = result_text
                    result['meta'] = ""
                    return result
                if state['return_message'] == 'want':
                    cur_text = state['history_user'][-1]
                    if 'да' in cur_text.lower() or 'хочу' in cur_text.lower() or 'конечно' in cur_text.lower():
                        state['return_to_id'] = 0
                        state['return_message'] = 'where_want'
                        result = {'text': 'В каком зале Вы сейчас находитесь?', 'meta':''}
                        return result
                    else:
                        return {'text': 'Чем Вы интересуетесь?', 'meta': ''}
            tokens, ners = models['ner_model']([text])
            tokens = np.array(tokens[0])
            ners = np.array(ners[0])
            mask = ners != 'O'
            lemmatize_text = lemmatize(text.lower())
            text_lemm_set = set(lemmatize_text.split())
            this_words = apply_lemm(['эта', 'это', 'эту', 'он', 'она', 'её', 'ее', 'его', 'та'])
            find_words = apply_lemm(['где', 'в каком зале', 'находится', 'висит', 'стоит', 'выставляется'])
            path_words = apply_lemm(['как пройти', 'пройти', 'путь', 'маршрут', 'построй'])
            toilet = apply_lemm(['туалет', 'гардероб', 'камера хранения', 'камера', 'хранения', 'уборная'])
            if len(set(toilet) & text_lemm_set) > 0:
                return {'text': 'Идите к лестнице, спуститесь на первый этаж. По лестнице у входа спуститесь ниже.', 'meta':''}
            elif len(set(find_words) & text_lemm_set) > 0:
                if state['history_object'] is not None and len(set(this_words) & text_lemm_set) > 0:
                    best_search = state['history_object']
                    state['history_user'][-1] = best_search['name']
                    print('Short path with history_object: {}'.format(best_search))
                else:
                    for i, cl in enumerate(ners):
                        if 'ORG' in cl:
                            mask[i] = False
                    search_queue = ['objects', ['name', 'authors'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                    print('Search queue: {}'.format(str(search_queue)))
                    search_result = models['search'](*search_queue)
                    best_search = search_result[0]
                    print('Search result: {}'.format(best_search))
                hall = best_search['hall']
                if hall == '':
                    return {'text': 'К сожалению, этот экспонат сейчас хранится в архиве, но Вы можете <a href="https://pushkinmuseum.art{}">посмотреть его на сайте Пушкинского музея</a>. Подсказать что-нибудь ещё?'.format(best_search['img'])}
                building = best_search['building']
                state['history_object'] = best_search
                if building == '117':
                    buld = 'gallery'
                else:
                    buld = 'main'
                result_text = "Вы можете найти экспонат \"{}\" в зале {}. Хотите ли Вы туда пройти?".format(str(best_search['name']), str(hall))
                state['return_to_id'] = 0
                state['return_message'] = 'want'
                result = {'text': result_text, 'meta': ""}
                return result
            elif len(set(path_words) & text_lemm_set) > 0:  # Хочу пройти к
                state['return_to_id'] = 0
                state['return_message'] = 'where'
                result = {'text': 'В каком зале Вы сейчас находитесь?', 'meta': ''}
                return result
            raise Exception()
        except:
            traceback.print_exc()
            if state['history_object'] is not None and len(state['history_object']['text']) > 10:
                result = {'text': models['squad_ru']([state['history_object']['text']], [state['history_user'][-1]])[0]}
                if len(result) > 0:
                    return result

            result = {'text': 'Я вас не понял. Давайте поговорим о чём-нибудь другом. Что Вам нравится?', 'meta':''}
            state['return_to_id'] = 3
            state['return_message'] = ''
            return result
