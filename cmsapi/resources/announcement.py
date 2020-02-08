import time

from flask import jsonify
from flask_restful import Resource, reqparse, inputs

from cmsapi.db import zodb


class Announcement(Resource):

    def __init__(self):
        print(zodb)
        self.zmscontent = zodb['Application']['unibe']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_site = '/unibe/portal/content/e681'
        self.default_meta = 'newsbox'
        self.announcements = []

        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('limit', type=int)
        self.parser.add_argument('search', type=str)
        self.parser.add_argument('site', type=str)
        #self.parser.add_argument('recursive', type=inputs.boolean)
        self.args = self.parser.parse_args()

    def get(self):
        self.query_announcements([])
        return jsonify(self.filter_announcements())

    def query_announcements(self, boxtype):

        # filter boxtype of newsbox elements
        if boxtype in ['news', 'events']:
            type_filter = boxtype
            type_filter = type_filter == 'events' and 'event' or 'news'
        else:
            type_filter = None

        site = self.args['site'] is not None and self.args['site'] or self.default_site

        print(site)
        elements = self.zmsindex({'meta_id': self.default_meta, 'path': site})  # {'get_uid': 'uid:578670f7-4985-473b-a79b-3f96dcdc9fdb'}
        print("total: {}".format(len(elements)))

        for i, e in enumerate(elements):
            obj = e.getObject()
            img = obj.attr('img')
            protocol = obj.getConfProperty('ASP.protocol', 'http')
            domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
            href = '{}://{}'.format(protocol, domain)
            announcement = {
                'uuid': e.get_uid.replace('uid:', ''),
                'path': e.getPath(),
                'type': obj.attr('boxtype'),
                'title': {
                    'de': obj.attr('title', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('title', REQUEST={'lang': 'eng'})
                },
                'text': {
                    'de': obj.attr('text', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('text', REQUEST={'lang': 'eng'})
                },
                'image': {
                    'de': (img is not None and not isinstance(img, str)) and href + obj.attr('img').getHref(REQUEST={'lang': 'ger'}) or '',
                    'en': (img is not None and not isinstance(img, str)) and href + obj.attr('img').getHref(REQUEST={'lang': 'eng'}) or ''
                },
                'infolink': {
                    'de': self.zmscontent.getLinkUrl(obj.attr('attr_url', REQUEST={'lang': 'ger'})),
                    'en': self.zmscontent.getLinkUrl(obj.attr('attr_url', REQUEST={'lang': 'eng'}))
                },
                'responsible': {
                    'de': obj.attr('attr_dc_creator', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('attr_dc_creator', REQUEST={'lang': 'eng'})
                },
                'keywords': {
                    'de': obj.attr('attr_dc_subject', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('attr_dc_subject', REQUEST={'lang': 'eng'})
                },
                'section': {
                    'de': obj.attr('attr_dc_subject_section', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('attr_dc_subject_section', REQUEST={'lang': 'eng'})
                },
                'topic': {
                    'de': obj.attr('attr_dc_subject_topic', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('attr_dc_subject_topic', REQUEST={'lang': 'eng'})
                },
                'eventdate': {
                    'de': self.zmscontent.getLangFmtDate(
                        obj.attr('attr_event_start', REQUEST={'lang': 'ger'}),
                        fmt_str='ISO8601'),
                    'en': self.zmscontent.getLangFmtDate(
                        obj.attr('attr_event_start', REQUEST={'lang': 'eng'}),
                        fmt_str='ISO8601')
                },
                'published': {
                    'from': {
                        'de': self.zmscontent.getLangFmtDate(
                            obj.attr('attr_active_start', REQUEST={'lang': 'ger'}),
                            fmt_str='ISO8601'),
                        'en': self.zmscontent.getLangFmtDate(
                            obj.attr('attr_active_start', REQUEST={'lang': 'eng'}),
                            fmt_str='ISO8601')
                    },
                    'until': {
                        'de': self.zmscontent.getLangFmtDate(
                            obj.attr('attr_active_end', REQUEST={'lang': 'ger'}),
                            fmt_str='ISO8601'),
                        'en': self.zmscontent.getLangFmtDate(
                            obj.attr('attr_active_end', REQUEST={'lang': 'eng'}),
                            fmt_str='ISO8601')
                    }
                }
            }

            try:
                active_parent = obj.getParentNode().isActive(REQUEST={'lang': 'ger'}) and 1 or 0
                active_self = obj.attr('active', REQUEST={'lang': 'ger'}) and 1 or 0
                available = obj.attr('attr_active_end', REQUEST={'lang': 'ger'})
                if available is not None:
                    available = time.mktime(available) >= time.time() and 1 or 0
                else:
                    available = 1
            except:
                active_parent = 0
                active_self = 0
                available = 0

            if active_parent and active_self and available and \
                    obj.attr('boxtype') == type_filter and True or type_filter is None and True or False:
                self.announcements.append(announcement)

        print("filtered: {}".format(len(self.announcements)))

    def filter_announcements(self):
        # order by date
        announcements = sorted(self.announcements, key=lambda k: k['eventdate']['de'], reverse=True)
        filtered_announcements = []

        search = self.args['search']
        if search is not None:
            for announcement in announcements:
                if announcement['title']['de'].lower().find(search.lower()) > -1:
                    filtered_announcements.append(announcement)
        else:
            filtered_announcements = announcements

        limit = self.args['limit']
        if limit is not None:
            # limit is set by the query string
            if limit > 0:
                return filtered_announcements[0:limit]
            # limit=0 returns all
            if limit == 0:
                return filtered_announcements
        # limit=100 is default
        return filtered_announcements[0:100]


class AnnouncementType(Announcement, Resource):

    def get(self, boxtype):
        self.query_announcements(boxtype)
        return jsonify(self.filter_announcements())
