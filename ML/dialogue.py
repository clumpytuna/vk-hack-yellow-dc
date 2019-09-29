import sys
sys.path.append('/home/iprovilkov/data/vk-hack-yellow-dc/')
from elastic_search import elastic_search
from deeppavlov import configs, build_model
from ml_utils import lemmatize, apply_lemm
from path_finder.path import find_path
from navigation_scenario import NavigationScenario
from culture_scenario import CultureScenario
from other_scenario import OtherScenario
from random_scenario import RandomScenario
import numpy as np


#NAVIGATION 
navigation_words = 'где находится туалет кафе камера хранения пройти карта столовая куда пойти идем зал найти путь'
navigation_phrases = ['в каком зале', 'где висит', 'где находится', 'где стоит', 'где найти', 'где выставляется', 'где посмотреть', 'как пройти', 'какой маршрут']

#CULTURE
culture_words = 'выставка картины скульптуры расскажи какой технике найди аудио дорожка скачать список покажи книга книги работа работах жанр годы друзья список изданий каталог почему покажите знаменитые расскажи кто страна РОССИЯ ЕВРОПА регион государство место город местечно край написала написать написал год'
culture_phrases = ['найти что-то', 'что есть', 'список изданий', 'что посмотреть', 'покажите предметы', 'у вас есть', 'знаменитые картины', 'откуда', 'есть ли','расскажи о', 'создатель', 'художник', 'скульптор']

#OTHER
other_words = 'будет будут дата январь февраль март апрель май июнь июль август сентябрь октябрь ноябрь декабрь'
other_phrases = ['что будет в', 'когда будет', 'когда будет выставка', 'дата проведения', 'когда проводится', 'какие выставки будут']

def make_find_set(words, phrases):
    lemmed_words = lemmatize(words.lower()).split()
    phrases = [phrase.lower() for phrase in phrases]
    find_set = set(lemmed_words + phrases)
    return find_set


find_sets = [make_find_set(navigation_words, navigation_phrases), 
             make_find_set(culture_words, culture_phrases), 
             make_find_set(other_words, other_phrases)]


def classify(text, find_sets):
    lemmed = lemmatize(text.lower())
    finded = np.zeros(len(find_sets))
    for i, find_set in enumerate(find_sets):
        for item in find_set:
            if item in lemmed or item in text:
                print('[debug] found item {} from set {} in lemma {}'.format(item, i, lemmed))
                finded[i] += 1
    result_class = np.argmax(finded)
    if ('давай познакомимся' in text.lower()) or ('давай поговорим' in text.lower()) or ('привет' in text.lower()) or ('добрый день' in text.lower()) or ('здравствуйте' in text.lower()):
        result_class = 3
    return result_class


class Dialogue:
    def __init__(self, find_sets, models):
        self.scenarios = [NavigationScenario(), CultureScenario(), OtherScenario(), RandomScenario()]
        self.find_sets = find_sets
        self.models = models
        self.state = {}
        self.state['history_user'] = []
        self.state['history_bot'] = []
        self.state['return_to_id'] = -1
        self.state['history_object'] = None
    
    def answer(self, text):
        self.state['history_user'].append(text)
        if self.state['return_to_id'] != -1:
            current_class = self.state['return_to_id']
        else:
            current_class = classify(text, self.find_sets)

        scenario = self.scenarios[current_class]
        print('\tscenario: ', type(scenario).__name__)
        print('\tstate:', str(self.state))
        return scenario.answer(self.state, self.models)
    

class DialogueHandler:
    #self.models
    #def process
    #    classify
    #self.dialogues = {request_id:Dialogue(state, models)}
    
    def __init__(self):
        self.models = {'search': elastic_search, 
                  'ner_model': build_model(configs.ner.ner_ontonotes_bert_mult, download=False),
                   'find_path': find_path,
                    'squad_ru': build_model(configs.squad.squad_ru_bert, download=False)}
        self.dialogues = {}
    
    def process(self, r):
        # r['id', 'request', 'meta']
        id_ = r['id']
        text = r['request']
        global find_sets
        if id_ not in self.dialogues:
            self.dialogues[id_] = Dialogue(find_sets, self.models)
        result = self.dialogues[id_].answer(text) # RETURNS {'text':, 'meta': }
        result['id'] = id_
        return result
