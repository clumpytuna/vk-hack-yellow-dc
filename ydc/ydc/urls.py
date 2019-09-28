from django.conf.urls import url

from ydc.views import create_dialogue, request_audio, request_text, response_audio, response_text

urlpatterns = [
    url(r'^create', create_dialogue),
    url(r'^request_audio', request_audio),
    url(r'^request_text', request_text),
    url(r'^response_audio', response_audio),
    url(r'^response_text', response_text),
]
