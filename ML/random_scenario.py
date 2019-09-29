from ml_utils import *
from dialogue import *
from path_finder.path import find_path
import numpy as np
import traceback


class RandomScenario(BaseScenario):
    # SCENARIO_ID=3
    def __init__(self):
        pass
    
    def answer(self, state, models):
        text = state['history_user'][-1]
        if 'xvf' in text.lower():
            return {'text':'Для незрячих и слабовидящих посетителей в рамках наиболее значимых выставок в музее предлагаются тактильные макеты экспонатов, образовательные программы. \n Инклюзивная программа к выставке "Щукин. Биография коллекции" организована в рамках проекта «Доступный музей» и включает в себя тактильные макеты по мотивам произведений «Танец» Анри Матисса, «Белые кувшинки» Клода Моне и другие. Макеты сопровождаются этикетками на шрифте Брайля, а также аудиогидом с тифлокомментированием.'}
        if 'отзыв' in text.lower():
            state['return_to_id'] = 3
            state['return_message'] = 'feedback'
            return {'text':'Пожалуйста говорите, ваше мнение важно для нас.'}
        try:
            # RETURNS
            if state['return_to_id'] == 3:
                state['return_to_id'] = -1
                state['return_message'] = ''
                if state['return_message'] == 'feedback':
                    return {'text':'Спасибо! Что еще вас интересует?'}
                tokens, ners = models['ner_model']([text])
                tokens = np.array(tokens[0])
                ners = np.array(ners[0])
                mask = ners != 'O'
                lemmatize_text = lemmatize(text.lower())
                text_lemm_set = set(lemmatize_text.split())
                search_queue = ['objects', ['name', 'text'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                print('Search queue: {}'.format(str(search_queue)))
                search_result = models['search'](*search_queue) 
                best_search = search_result[0]
                print('Search result: {}'.format(best_search))
                result_text = "Рекомендую посмотреть экспонат \"" + str(best_search['name']) + "\". Подсказать что-нибудь ещё?"
                state['history_object'] = best_search
                return {'text':result_text}
            # Returns
            state['return_to_id'] = 3
            return {'text': "Что вам нравится?"}
        except:
            traceback.print_exc()
            if state['history_object'] is not None and len(state['history_object']['text']) > 10:
                result = {'text': models['squad_ru']([state['history_object']['text']], [state['history_user'][-1]])[0]}
                if len(result['text'][0]) > 0:
                    return result

            result = {'text': 'Я вас не понял. Давайте поговорим о чём-нибудь другом. Что Вам нравится?', 'meta': ''}
            state['return_to_id'] = 3
            state['return_message'] = ''
            return result
