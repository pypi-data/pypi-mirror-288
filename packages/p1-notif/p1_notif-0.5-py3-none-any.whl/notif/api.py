
from builtins import object
import json
import requests

from .constants import K_NOTIF_API_KEY
from .constants import K_NOTIF_API_URL


class NotifApi(object):

    def __init__(self, api_key=K_NOTIF_API_KEY):
        self.notif_service_url = K_NOTIF_API_URL
        self.api_key = api_key

    def bulk_send(self, notifications, is_async=False):
        notification_body_list = []
        attachments = []
        for index, notif in enumerate(notifications):
            notification_body_list += [{
                'data': notif.json(),
                'type': notif.notif_type(),
                'is_async': is_async,
            }]
            for attachment in notif.attachments():
                attachments += [('attachment_%d' % index, attachment)]
        body = json.dumps(notification_body_list)

        if len(attachments) > 0:
            response = requests.post(
                self.notif_service_url,
                data={'body': body},
                headers={'API-KEY': self.api_key},
                files=attachments
            )
        else:
            response = requests.post(
                self.notif_service_url,
                headers={
                    'Content-Type': 'application/json',
                    'API-KEY': self.api_key,
                },
                data=body,
            )

        if response.status_code != requests.codes.ok:
            raise Exception('failed send bulk notif ' + response.text)

    def send(self, notification, is_async=False):
        self.bulk_send(notifications=[notification], is_async=is_async)
