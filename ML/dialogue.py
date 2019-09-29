import sys
sys.path.append('/home/captain/vk-hack-yellow-dc/')
from elastic_search import elastic_search
from deeppavlov import configs, build_model
from ml_utils import lemmatize, apply_lemm
from path_finder.path import find_path
from navigation_scenario import NavigationScenario
import numpy as np


#NAVIGATION 
navigation_words = 'где находится туалет кафе камера хранения пройти карта столовая куда пойти идем зал найти путь'
navigation_phrases = ['в каком зале', 'где висит', 'где стоит', 'где найти', 'где выставляется', 'где посмотреть', 'как пройти', 'какой маршрут']

#CULTURE

#OTHER

def make_find_set(words, phrases):
    lemmed_words = lemmatize(words.lower()).split()
    phrases = [phrase.lower() for phrase in phrases]
    find_set = set(lemmed_words + phrases)
    return find_set


find_sets = [make_find_set(navigation_words, navigation_phrases), set(), set()]


def classify(text, find_sets):
    lemmed = lemmatize(text.lower())
    finded = np.zeros(len(find_sets))
    for i, find_set in enumerate(find_sets):
        for item in find_set:
            if item in lemmed:
                finded[i] += 1
    result_class = np.argmax(finded)
    return result_class


class Dialogue:
    def __init__(self, find_sets, models):
        self.scenarios = [NavigationScenario(), NavigationScenario(), NavigationScenario()]
        self.find_sets = find_sets
        self.models = models
        self.state = {}
        self.state['history_user'] = []
        self.state['history_bot'] = []
        self.state['return_to_id'] = -1
    
    def answer(self, text):
        self.state['history_user'].append(text)
        if self.state['return_to_id'] != -1:
            current_class = self.state['return_to_id']
        else:
            current_class = classify(text, self.find_sets)

        return self.scenarios[current_class].answer(self.state, self.models)
    

class DialogueHandler:
    #self.models
    #def process
    #    classify
    #self.dialogues = {request_id:Dialogue(state, models)}
    
    def __init__(self):
        self.models = {'search': elastic_search, 
                  'ner_model': build_model(configs.ner.ner_ontonotes_bert_mult, download=False),
                   'find_path': find_path}
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
