from ml_utils import *
from dialogue import *
import numpy as np
import traceback
from datetime import datetime
from typing import List, Dict

def parse_date(date):
    if date.startswith('0000-00-00'):
        return None
    else:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()


def init_events():
    import requests
    # events0 = json.load(open('../../data/events.json'))
    events0 = requests.get('https://pushkinmuseum.art/json/events.json')
    events0 = events0.json()

    events = []
    for event_key, event in events0.items():
        date_begin = parse_date(event['dateBegin'])
        date_end = parse_date(event['dateEnd'])
        if date_begin is None:
            continue
        if date_end is None:
            date_end = date_begin
        events.append((date_begin, date_end, event))
    events.sort(key=lambda event_tuple: event_tuple[1] - event_tuple[0])
    events = [(str(date_begin), str(date_end), event) for date_begin, date_end, event in events]
    return events


events = init_events()


def find_events(date_begin: str, date_end: str) -> List[Dict]:
    def is_date_inside(date, begin, end):
        return begin <= date <= end

    events_filtered = [
        event for event_date_begin, event_date_end, event in events if
        is_date_inside(date_begin, event_date_begin, event_date_end) or
        is_date_inside(date_end, event_date_begin, event_date_end)
    ]
    return events_filtered

class OtherScenario(BaseScenario):
    # SCENARIO_ID=2
    def __init__(self):
        pass
    
    def answer(self, state, models):
        text = state['history_user'][-1]
        tokens, ners = models['ner_model']([text])
        tokens = np.array(tokens[0])
        ners = np.array(ners[0])
        mask = ners != 'O'
        lemmatize_text = lemmatize(text.lower())
        text_lemm_set = set(lemmatize_text.split())

        # вопросы вида "Что будет 11 октября?"
        if any('DATE' in ner for ner in ners):
            year = 2019
            month = None
            day = None

            tokens_date = [token for token, ner in zip(tokens, ners) if 'DATE' in ner]

            months = 'январь февраль март апрель май июнь июль август сентябрь октябрь ноябрь декабрь'.split()
            possible_months = text_lemm_set & set(months)
            month = next(iter(possible_months)) if possible_months else None
            if not month:
                return {text: 'todo1', meta: ''}
            month = 1 + months.index(month)

            days = set([str(i) for i in range(1, 31 + 1)])
            possible_days = (text_lemm_set | set(tokens)) & set(days)
            day = int(next(iter(possible_days))) if possible_days else None

            date_begin = '{}-{:02}-{:02}'.format(year, month, day if day else 1)
            date_end = '{}-{:02}-{:02}'.format(year, month, day if day else 31)
            print(date_begin, '-', date_end)

            events = find_events(date_begin, date_end)
            events = [event for event in events if 'ru' in event['name']]
            events = events[:3]
            if events:
                text = '.\n\n'.join([event['name']['ru'] for event in events]) + '.'
                return {'text': text, 'meta': ''}
            else:
                return {'text': 'Не нашлось событий :(', 'meta': ''}
           
        # вопросы вида "Когда будет выставка восточный джаз?"
        when_words = apply_lemm(['выставка', 'концерт', 'лекция', 'мероприятие', 'экскурсия'])
        when_phrases = ['когда будет', 'когда проходит', 'когда состоится']
        if len(set(when_words) & text_lemm_set) > 0 or any(phrase in text for phrase in when_phrases):
            search_queue = ['events', ['text'], text]
            print('Search queue: {}'.format(str(search_queue)))
            search_result = models['search'](*search_queue)
            best_search = search_result[0]
            print('Search result: {}'.format(best_search)[:80])
            
            def format_date(date):
                months_в_родительном = 'января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
                month = months_в_родительном[date.month - 1]
                return '{} {}'.format(date.day, month)
            
            event = best_search
            date_begin = parse_date(event['dateBegin'])
            date_end = parse_date(event['dateEnd'])
            text_when = format_date(date_begin) if date_end is None else 'с {} по {}'.format(format_date(date_begin), format_date(date_end))
            text = '{} "{}" будет проходить {}'.format(event['type'], event['name'], text_when)
            return {'text': text, 'meta': ''}

        return {'text': 'todo2', 'meta': ''}