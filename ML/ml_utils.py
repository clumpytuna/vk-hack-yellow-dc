import os
import pymorphy2
import re
import chardet
from nltk.tokenize import WordPunctTokenizer
import numpy as np


class BaseScenario:
    def __init__(self):
        pass
    
    def answer(self, state):
        pass


def lemmatize(text):
    text = " ".join(word.lower() for word in text.split()) #lowercasing and removing short words 
    text = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', text) #deleting newlines and line-breaks
    text = re.sub('[.,:;%©?*,!@#$%^&()\d]|[+=]|[[]|[]]|[/]|"|\s{2,}|-', ' ', text) #deleting symbols  
    text = " ".join(pymorphy2.MorphAnalyzer().parse(word)[0].normal_form for word in text.split())
    return text

def apply_lemm(lst):
    return [lemmatize(word) for word in lst]
