#!/usr/bin/env python3

import pika
from json import dumps, loads
from dialogue import DialogueHandler

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
    result = handler.process(r)
    channel_send.basic_publish(
            exchange='',
            routing_key=QUEUE_RESPONSES,
            body=dumps({
                'id': result['id'],
                'response': result['request'],
                'meta': result['meta'],
            })
    )
    print("SENT: id '{}', request '{}', meta '{}'".format(r['id'], r['request'], r['meta']))


def main():
    _prepare()

    channel_receive.basic_consume(QUEUE_REQUESTS, _callback, auto_ack=True)

    channel_receive.start_consuming()


if __name__ == '__main__':
    main()
