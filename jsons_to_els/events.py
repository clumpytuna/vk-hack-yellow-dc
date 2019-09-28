#!/usr/bin/env python3

import requests
import sys
import json


URL_ELS_WITH_FORMAT = 'http://localhost:9200/{}/_doc/{}'


def send_json_to_els(index: str, data_id: str, data: str):
    return requests.post(URL_ELS_WITH_FORMAT.format(index, data_id), data=data, headers={'Content-Type': 'application/json'})


def nonize_field(data: dict, key: str):
    if data.get(key) is not None and data[key] == '':
        data[key] = None


def main():
    if len(sys.argv) < 3:
        print("Syntax: ./events.py <file> <index_in_elastic>")
        return

    with open(sys.argv[1], 'r') as f:
        raw = f.read()

    index = sys.argv[2]

    jsons = json.loads(raw)
    for data_id in jsons.keys():
        data = jsons[data_id]

        # Special operations
        del data['searcha']

        # Normalization
        for field in data.keys():
            nonize_field(data, field)

        response = send_json_to_els(index, data_id, json.dumps(data))
        print("Result for #{}: Code {}, Content {}".format(data_id, response.status_code, str(response.content)))


if __name__ == '__main__':
    main()
