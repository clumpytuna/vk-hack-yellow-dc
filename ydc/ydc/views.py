import logging
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .speech_kit import speech_to_text
from .models_dialogue import Dialogue
from .dialogue_processor import process_dialogue

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_423_LOCKED

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_dialogue(request) -> Response:
    """
    Allocate a new Dialogue object
    """
    dialogue = Dialogue(ts=datetime.now())
    dialogue.save()
    dialogue.refresh_from_db()
    return Response({'id': str(dialogue.id)})


@api_view(['POST'])
def request_text(request) -> Response:
    """
    Make request to the system, providing text
    """
    try:
        d_id = int(request.POST['id'])
        dialogue = Dialogue.objects.get(id=d_id)
    except KeyError or ValueError:
        return Response('Dialogue ID is not present in the request or is not a valid Dialogue ID', HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(None, HTTP_404_NOT_FOUND)

    try:
        text = request.POST['request']
    except KeyError:
        return Response('Request is not present in the request', HTTP_400_BAD_REQUEST)

    dialogue.add_request(text)

    # Entry point processing call
    process_dialogue(dialogue)

    return Response(None)


@api_view(['POST'])
def request_audio(request) -> Response:
    """
    Make request to the system, providing OGG
    """
    try:
        d_id = int(request.POST['id'])
        dialogue = Dialogue.objects.get(id=d_id)
    except KeyError or ValueError:
        return Response('Dialogue ID is not present in the request or is not a valid Dialogue ID', HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(None, HTTP_404_NOT_FOUND)

    try:
        speech = request.FILES['speech'].read()
    except KeyError:
        return Response("'speech' parameter with OGG file must be set for this API.", HTTP_400_BAD_REQUEST)

    text = speech_to_text(speech)
    if text is None or text.isspace():
        return Response(None)

    dialogue.add_request(text)

    # Entry point processing call
    process_dialogue(dialogue)

    return Response(None)


@api_view(['POST'])
def response_text(request) -> Response:
    """
    Get textual response from the server
    """
    try:
        d_id = int(request.POST['id'])
        dialogue = Dialogue.objects.get(id=d_id)
    except KeyError or ValueError:
        return Response('Dialogue ID is not present in the request or is not a valid Dialogue ID', HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(None, HTTP_404_NOT_FOUND)

    if dialogue.response is None:
        return Response('There is no response for this dialogue (yet?)', HTTP_423_LOCKED)

    return Response(dialogue.response, content_type='text/plain')


@api_view(['POST'])
def response_audio(request) -> HttpResponse:
    """
    Get textual response from the server
    """
    try:
        d_id = int(request.POST['id'])
        dialogue = Dialogue.objects.get(id=d_id)
    except KeyError or ValueError:
        return Response('Dialogue ID is not present in the request or is not a valid Dialogue ID', HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(None, HTTP_404_NOT_FOUND)

    ogg = dialogue.load_ogg()
    if ogg is None:
        return Response('There is no audio response for this dialogue (yet?)', HTTP_423_LOCKED)

    response = HttpResponse(ogg, content_type='audio/ogg')
    return response
