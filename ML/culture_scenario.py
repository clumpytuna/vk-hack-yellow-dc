from ml_utils import *
from dialogue import *
from path_finder.path import find_path
import numpy as np
import traceback


class CultureScenario(BaseScenario):
    # SCENARIO_ID=1
    def __init__(self):
        pass
    
    def answer(self, state, models):
        text = state['history_user'][-1]
        try:
            # RETURNS
            if state['return_to_id'] == 1:
                pass
            # Returns

            tokens, ners = models['ner_model']([text])
            tokens = np.array(tokens[0])
            ners = np.array(ners[0])
            mask = ners != 'O'
            lemmatize_text = lemmatize(text.lower())
            text_lemm_set = set(lemmatize_text.split())

            narrative_words = apply_lemm(['что', 'расскажи о', 'опиши', 'техника', 'покажите', 'аудио', 'книга', 'коллекция'])
            time_words = apply_lemm(['когда', 'время', 'изготовлен', 'произведен', 'написана', 'года', 'год', 'эпоха'])
            author_words = apply_lemm(['автор', 'кто', 'создатель', 'художник', 'скульптор'])
            country_words = apply_lemm(['где', 'в какой', 'страна', 'регион', 'государство', 'место', 'город', 'местечно', 'край'])

            if len(set(narrative_words) & text_lemm_set) > 0:
                print("Narrative case")
                for i, cl in enumerate(ners):
                    if 'ORG' in cl:
                        mask[i] = False
                if apply_lemm(['коллекция'])[0] in text_lemm_set: 
                    search_queue = ['collects', ['name', 'text'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                else:
                    search_queue = ['objects', ['name', 'text'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                print('Search queue: {}'.format(str(search_queue)))
                search_result = models['search'](*search_queue) 
                best_search = search_result[0]
                print('Search result: {}'.format(best_search))
                result_text = best_search['text']
                state['history_object'] = best_search
                return {'text':result_text}
            if len(set(time_words) & text_lemm_set) > 0:
                print("Date case")
                search_queue = ['objects', ['name', 'text'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                print('Search queue: {}'.format(str(search_queue)))
                search_result = models['search'](*search_queue) 
                best_search = search_result[0]
                print('Search result: {}'.format(best_search))
                result_text = "Данное произведение было создано в " + str(best_search['year']) + " году."
                state['history_object'] = best_search
                return {'text':result_text}
            if len(set(author_words) & text_lemm_set) > 0:
                print("Author case")
                search_queue = ['objects', ['name', 'text'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                print('Search queue: {}'.format(str(search_queue)))
                search_result = models['search'](*search_queue) 
                best_search = search_result[0]
                print('Search result: {}'.format(best_search))
                result_text = "Автор данной работы - " + str(best_search['authors'][0]) + "."
                state['history_object'] = best_search
                return {'text':result_text}
            if len(set(country_words) & text_lemm_set) > 0:
                search_queue = ['objects', ['name', 'text'], ' '.join(tokens[mask]) if len(tokens[mask]) != 0 else text]
                print('Search queue: {}'.format(str(search_queue)))
                search_result = models['search'](*search_queue) 
                best_search = search_result[0]
                print('Search result: {}'.format(best_search))
                result_text = "Произведение было создано в стране " + str(best_search['country']) + '.'
                state['history_object'] = best_search
                return {'text':result_text}
            raise Exception()
        except:
            traceback.print_exc()
            if state['history_object'] is not None and len(state['history_object']['text']) > 10:
                result = {'text': models['squad_ru']([state['history_object']['text']], [state['history_user'][-1]])[0]}
            else:
                result = {'text': 'Я вас не понял. Давайте поговорим о чём-нибудь другом.', 'meta':''}
            return result
