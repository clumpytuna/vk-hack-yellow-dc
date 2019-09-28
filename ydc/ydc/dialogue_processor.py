import json

from .models_dialogue import Dialogue
from .speech_kit import text_to_speech


def process_dialogue(dialogue: Dialogue):
    """
    Main pipeline.
    During and after processing, dialogue is changed in DB, and as an object
    :param dialogue: dialogue to process
    """
    # "echo"
    dialogue.response = dialogue.request
    ogg = text_to_speech(dialogue.request)
    dialogue.save_ogg(ogg)

    dialogue.save()
    dialogue.refresh_from_db()
