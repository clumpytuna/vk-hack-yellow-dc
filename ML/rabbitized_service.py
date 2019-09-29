#!/usr/bin/env python3

import pika
from json import dumps, loads
from dialogue import DialogueHandler

import traceback

QUEUE_REQUESTS = 'request'
QUEUE_RESPONSES = 'response'
handler = DialogueHandler()

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
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='demo134.bravo.vkhackathon.com', credentials=credentials))

    channel_send = connection.channel()
    channel_send.queue_declare(queue=QUEUE_RESPONSES)

    channel_receive = connection.channel()
    channel_receive.queue_declare(queue=QUEUE_REQUESTS)


def _callback(channel, method, properties, body):
    r = loads(body)
    print("RECIEVED: id '{}', request '{}', meta '{}'".format(r['id'], r['request'], r['meta']))

    # Handler here
    global handler
    try:
        result = handler.process(r)
    except:
        traceback.print_exc()
        result = {'id': r['id'], 'text': 'Ничего не нашлось :-(', 'meta': ''}

    result_to_return = {
        'id': result['id'],
        'response': result['text'],
        'meta': result.get('meta', ''),
    }
    channel_send.basic_publish(
            exchange='',
            routing_key=QUEUE_RESPONSES,
            body=dumps(result_to_return)
    )
    print("SENT: {}".format(str(result_to_return)))


def main():
    _prepare()

    channel_receive.basic_consume(QUEUE_REQUESTS, _callback, auto_ack=True)
    
    print('Starting to consume requests')
    channel_receive.start_consuming()


if __name__ == '__main__':
    main()

