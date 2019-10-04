import pika
from json import dumps, loads

from django.core.exceptions import ObjectDoesNotExist

from .models_dialogue import Dialogue


QUEUE_REQUESTS = 'request'
QUEUE_RESPONSES = 'response'


connection = None
channel_send = None
channel_receive = None


def _prepare():
    """
    Prepare pika connection
    """
    global connection
    global channel_send
    global channel_receive

    credentials = pika.PlainCredentials('ydc', 'ydcpasswd')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='ec2-52-59-255-231.eu-central-1.compute.amazonaws.com', credentials=credentials))

    channel_send = connection.channel()
    channel_send.queue_declare(queue=QUEUE_REQUESTS)

    channel_receive = connection.channel()
    channel_receive.queue_declare(queue=QUEUE_RESPONSES)


def send_to_rabbit(dialogue: Dialogue):
    """
    Send request via RabbitMQ
    """
    global channel_send
    _prepare()

    channel_send.basic_publish(
            exchange='',
            routing_key=QUEUE_REQUESTS,
            body=dumps({'id': dialogue.id, 'request': dialogue.request, 'meta': dialogue.meta})
    )


def receive_from_rabbit(dialogue: Dialogue) -> Dialogue:
    """
    Receive request from RabbitMQ.
    Dialogue and other dialogues may be updated in the database
    """
    dialogue_from_db = Dialogue.objects.get(id=dialogue.id)
    if dialogue_from_db.rabbit_updated:
        dialogue_from_db.rabbit_updated = False
        dialogue_from_db.save()
        return dialogue_from_db

    global channel_receive
    _prepare()

    while True:
        ok, prop, body = channel_receive.basic_get(queue=QUEUE_RESPONSES, auto_ack=True)
        if ok is None:
            # break
            continue

        rabbit_response = loads(body)
        print('RECEIVED {}'.format(rabbit_response))
        try:
            current_dialogue = Dialogue.objects.get(id=int(rabbit_response['id']))
        except ObjectDoesNotExist:
            continue
        current_dialogue.response = rabbit_response.get('response')
        current_dialogue.meta = rabbit_response.get('meta', '')

        if current_dialogue.id == dialogue.id:
            current_dialogue.rabbit_updated = False
        else:
            current_dialogue.rabbit_updated = True

        current_dialogue.save()
        if current_dialogue.id == dialogue.id:
            return current_dialogue
