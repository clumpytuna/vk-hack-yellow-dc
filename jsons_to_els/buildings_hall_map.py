#!/usr/bin/env python3

import sys
import json


def main():
    if len(sys.argv) < 2:
        print("Syntax: ./buildings_hall_map.py <file>")
        return

    with open(sys.argv[1], 'r') as f:
        raw = f.read()

    result = {}

    jsons = json.loads(raw)
    for data_id in jsons.keys():
        data = jsons[data_id]

        if data['floors'] == '':
            continue

        for floor in data['floors'].keys():
            for hall in data['floors'][floor]['halls'].keys():
                result[hall] = data['floors'][floor]['halls'][hall]['number']

    print(result)


if __name__ == '__main__':
    main()
