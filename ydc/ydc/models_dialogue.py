import os
import logging

from django.db import models

from .settings import RESPONSES_OGG_DIRECTORY


logger = logging.getLogger(__name__)


class Dialogue(models.Model):
    id = models.AutoField(primary_key=True)
    ts = models.DateTimeField(null=False, help_text='Created')
    meta = models.TextField(null=False, default='', help_text='Arbitrary JSON-encoded metadata for this dialogue')
    request = models.TextField(null=True, help_text='Current question (text)')
    response = models.TextField(null=True, help_text='Current response (text)')
    _audio_response = models.TextField(null=True, help_text='FS path to current response (path to audio)')
    rabbit_updated = models.BooleanField(null=False, default=False)

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
