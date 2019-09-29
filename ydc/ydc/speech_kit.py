"""
Interaction with Yandex Speech Kit
"""

import logging
import requests

from .settings import SPEECHKIT_API_KEY

logger = logging.getLogger(__name__)


# TODO: Get from env


URL_RECOGNIZE = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
URL_RECOGNIZE_OPTIONS = '?topic=general'

HEADERS_RECOGNIZE = {
    'Authorization': 'Api-Key {}'.format(SPEECHKIT_API_KEY),
    'Content-Type': 'application/octet-stream'
}


URL_SYNTHESIZE = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
URL_SYNTHESIZE_OPTIONS = '?lang=ru-RU'

HEADERS_SYNTHESIZE = {
    'Authorization': 'Api-Key {}'.format(SPEECHKIT_API_KEY),
    'Content-Type': 'application/x-www-form-urlencoded'
}


def speech_to_text(speech: bytes) -> str:
    response = requests.post(URL_RECOGNIZE + URL_RECOGNIZE_OPTIONS, data=speech, headers=HEADERS_RECOGNIZE)

    if response.status_code != 200:
        logger.error('Speech Kit responded with code {}. Content: {}'.format(response.status_code, response.text))
        raise Exception('Speech recognition error')

    return response.json().get('result')


def text_to_speech(text: str) -> bytes:
    response = requests.post(URL_SYNTHESIZE + URL_SYNTHESIZE_OPTIONS, data={'text': text, 'voice': 'ermil', 'emotion': 'good'}, headers=HEADERS_SYNTHESIZE)

    if response.status_code != 200:
        logger.error('Speech Kit responded with code {}. Content: {}'.format(response.status_code, response.text))
        raise Exception('Speech synthesis error')

    return response.content
