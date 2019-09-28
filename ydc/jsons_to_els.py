import requests
import sys
import json


URL_ELS_WITH_FORMAT = 'localhost:9200/{}/_doc/{}'


def send_json_to_els(index: str, data_id: str, data: str):
    return requests.post(URL_ELS_WITH_FORMAT.format(index, data_id), data=data)


def main():
    with open(sys.argv[1], 'r') as f:
        raw = f.read()

    jsons = json.loads(raw)
    print(jsons.keys)


if __name__ == '__main__':
    main()
