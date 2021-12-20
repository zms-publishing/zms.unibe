import http
import requests

from flask import jsonify
from flask_restful import Resource

from cmsapi.resources.announcement import api


@api.route('/agenda/', endpoint='announcements_agenda')
class AnnouncementAgenda(Resource):

    def __init__(self):
        self.agenda_url = 'https://agenda.unibe.ch/agenda.json'
        self.agenda_path = '/unibe/portal/content/e299592'
        self.agenda_uuid = '271a321e-993e-4e36-b9a1-5b1f1d35e7f5'
        self.agenda_error = ''
        self.elements = []
        self.announcements = []
        try:
            result = requests.get(self.agenda_url, timeout=3)
            result.raise_for_status()
            self.elements = result.json()
        except requests.exceptions.RequestException as error:
            self.agenda_error = error

    def get(self):
        """
        Retrieve events from agenda.unibe.ch
        ---
        tags:
            - News and Events
        responses:
            200:
                description: OK
            204:
                description: No events found
            404:
                description: Problem with connection to agenda.unibe.ch
        """
        if self.query_announcements():
            return jsonify(self.filter_announcements())
        if self.agenda_error != '':
            return str(self.agenda_error), http.HTTPStatus.NOT_FOUND
        return '', http.HTTPStatus.NO_CONTENT

    def query_announcements(self):
        for i, e in enumerate(self.elements):
            announcement = {
                'type': 'event',
                'title': {
                    'de': e['veranstaltung_titel'],
                    'en': e['veranstaltung_titel'],
                },
                'topic': {
                    'de': e['veranstaltung_zyklus'],
                    'en': e['veranstaltung_zyklus'],
                },
                'infolink': {
                    'de': e['veranstalter_info_link'],
                    'en': e['veranstalter_info_link'],
                },
                'eventdate': {
                    'de': e['json_datum_zeit_start'],
                    'en': e['json_datum_zeit_start'],
                },
                'eventend': {
                    'de': e['json_datum_zeit_end'],
                    'en': e['json_datum_zeit_end'],
                },
                'eventinfo': {
                    'speakers': {
                        'de': e["veranstaltung_referenten"],
                        'en': e["veranstaltung_referenten"],
                    },
                    'location': {
                        'de': e["veranstaltung_ort"],
                        'en': e["veranstaltung_ort"],
                    },
                    'building': {
                        'de': e["veranstaltung_gebaude_adresse"],
                        'en': e["veranstaltung_gebaude_adresse"],
                    },
                    'room': {
                        'de': e["veranstaltung_horsaal"],
                        'en': e["veranstaltung_horsaal"],
                    }
                }
            }
            self.announcements.append(announcement)

        if len(self.announcements) > 0:
            return True
        return False

    def filter_announcements(self):
        # order by eventdate
        announcements = sorted(self.announcements, key=lambda k: k['eventdate']['de'], reverse=False)
        return announcements
