from django.conf.urls import url

from ydc.views import process_question

urlpatterns = [
    url(r'^process$', process_question)
]
