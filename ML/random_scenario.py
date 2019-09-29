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
        try:
            # RETURNS
            if state['return_to_id'] == 3:
                state['return_to_id'] = -1
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
            if len(state['history_object']['text']) > 10:
                result = {'text': models['squad_ru']([state['history_object']['text']], [state['history_user'][-1]])[0]}
            else:
                result = {'text': 'Я вас не понял. Давайте поговорим о чём-нибудь другом.', 'meta':''}
            return result
