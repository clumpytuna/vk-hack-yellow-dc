from django.http import HttpResponse

from .speech_kit import speech_to_text, text_to_speech

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


@api_view(['POST'])
def process_question(request):
    try:
        speech = request.FILES['speech'].read()
    except KeyError:
        return Response("'speech' parameter with OGG file must be set for this API.", HTTP_400_BAD_REQUEST)

    text = speech_to_text(speech)

    # Do something in our pipeline...

    result = text_to_speech(text)

    response = HttpResponse(result, content_type='audio/ogg')
    return response
