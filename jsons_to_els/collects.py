#!/usr/bin/env python3

import requests
import sys
import json


URL_ELS_WITH_FORMAT = 'http://localhost:9200/{}/_doc/{}'


def send_json_to_els(index: str, data_id: str, data: str):
    return requests.post(URL_ELS_WITH_FORMAT.format(index, data_id), data=data.encode('utf-8'), headers={'Content-Type': 'application/json'})


def nonize_field(data: dict, key: str):
    if data.get(key) is not None and data[key] == '':
        data[key] = None


def main():
    if len(sys.argv) < 3:
        print("Syntax: ./collects.py <file> <index_in_elastic>")
        return

    with open(sys.argv[1], 'r') as f:
        raw = f.read()

    index = sys.argv[2]

    jsons = json.loads(raw)
    for data_id in jsons.keys():
        data = jsons[data_id]
        object_result = {
            'path': data['path'],
            'name': data['name']['ru'],
            'text': data['text']['ru'],
            'img': data['circ_img']['id01'],
        }

        object_dumped = json.dumps(object_result, ensure_ascii=False)
        print("Object {}\n{}".format(data_id, object_dumped))

        response = send_json_to_els(index, data_id, object_dumped)
        print("Add to Elastic: Code {}, Content {}".format(response.status_code, str(response.content)))


if __name__ == '__main__':
    main()
