import requests
import json


ELASTIC_URL_TO_FORMAT = 'http://demo134.bravo.vkhackathon.com:9200/{}/_search'


def elastic_search(dataset: str, fields: list, query: str) -> list:
    """
    Search in ElasticSearch
    :param dataset: ES index
    :param fields: Document fields (ORed in search)
    :param query: Search query
    :return: a list of objects matching the given query, without elastic-specific fields
    """

    request = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': fields,
            }
        }
    }

    raw_response = requests.get(ELASTIC_URL_TO_FORMAT.format(dataset), data=json.dumps(request, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json'})
    if raw_response.status_code != 200:
        raise Exception(str(raw_response))
    response = raw_response.json()

    if response['hits']['total']['value'] == 0:
        raise ValueError()

    return [h['_source'] for h in response['hits']['hits']]
