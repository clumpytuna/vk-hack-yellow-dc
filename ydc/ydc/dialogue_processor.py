from .models_dialogue import Dialogue
from .speech_kit import text_to_speech
from .api_rabbit import send_to_rabbit, receive_from_rabbit


def process_dialogue(dialogue: Dialogue):
    """
    Main pipeline.
    During and after processing, dialogue is changed in DB, and as an object
    :param dialogue: dialogue to process
    """
    # "echo" + RabbitMQ check
    send_to_rabbit(dialogue)

    dialogue.response = dialogue.request
    ogg = text_to_speech(dialogue.request)
    dialogue.save_ogg(ogg)

    dialogue.save()
    dialogue.refresh_from_db()
