from .models_dialogue import Dialogue
from .speech_kit import text_to_speech
from .api_rabbit import send_to_rabbit, receive_from_rabbit


def process_dialogue(dialogue: Dialogue):
    """
    Main pipeline.
    During and after processing, dialogue is changed in DB, and as an object
    :param dialogue: dialogue to process
    """
    # Synchronous send and receive from RabbitMQ
    send_to_rabbit(dialogue)
    processed_dialogue = receive_from_rabbit(dialogue)
    if processed_dialogue is None or processed_dialogue.response is None or processed_dialogue.response.isspace():
        return

    ogg = text_to_speech(processed_dialogue.response)
    processed_dialogue.save_ogg(ogg)
    processed_dialogue.save()

    dialogue.refresh_from_db()
