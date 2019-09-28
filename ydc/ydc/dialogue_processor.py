import json

from .models_dialogue import Dialogue
from .speech_kit import text_to_speech


def process_dialogue(dialogue: Dialogue):
    """
    Main pipeline.
    During and after processing, dialogue is changed in DB, and as an object
    :param dialogue: dialogue to process
    """
    requests = json.loads(dialogue.requests)

    current_question = requests['raw'][-1]

    # "echo"
    dialogue.response = current_question
    ogg = text_to_speech(current_question)
    dialogue.save_ogg(ogg)

    dialogue.requests = json.dumps(requests)
    dialogue.save()
    dialogue.refresh_from_db()
