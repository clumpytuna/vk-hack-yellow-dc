import json
import os
import logging

from django.db import models

from .settings import RESPONSES_OGG_DIRECTORY


logger = logging.getLogger(__name__)


class Dialogue(models.Model):
    DEFAULT_REQUESTS = json.dumps({
        'version': 1,
        'raw': [],
    })

    id = models.AutoField(primary_key=True)
    ts = models.DateTimeField(null=False, help_text='Created')
    requests = models.TextField(null=False, default=DEFAULT_REQUESTS, help_text='Requests by user, JSON-encoded')
    response = models.TextField(null=True, help_text='Current response (text)')
    _audio_response = models.TextField(null=True, help_text='FS path to current response (audio)')

    def add_request(self, request: str):
        requests = json.loads(self.requests)

        requests['raw'].append(request)

        self.requests = json.dumps(requests)

    def save_ogg(self, b: bytes):
        if self._audio_response is not None:
            try:
                os.remove(self._audio_response)
            except:
                logging.warn('File removal error for path {}'.format(self._audio_response))

        self._audio_response = RESPONSES_OGG_DIRECTORY + str(self.id)

        with open(self._audio_response, 'wb') as f:
            f.write(b)

    def load_ogg(self):
        if self._audio_response is None:
            return None

        with open(self._audio_response, 'rb') as f:
            b = f.read()

        return b
