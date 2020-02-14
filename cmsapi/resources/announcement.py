import time

from flask import jsonify
from flask_restful import Resource, reqparse, inputs

from cmsapi.db import zodb


class Announcement(Resource):

    def __init__(self):
        print(zodb)
        self.zmscontent = zodb['Application']['unibe']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_path = '/unibe/portal/content/e681'
        self.default_uuid = '581e2cf8-fe7f-4e72-898d-92512d9596f0'
        self.default_meta = 'newsbox'
        self.default_limit = 50
        self.announcements = []

        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('limit', type=int)
        self.parser.add_argument('search', type=str)
        self.parser.add_argument('site', type=str)
        #self.parser.add_argument('recursive', type=inputs.boolean)
        self.args = self.parser.parse_args()

    def get(self, uuid=None):
        print uuid
        if self.query_announcements(uuid=uuid):
            return jsonify(self.filter_announcements())
        return 'Empty response', 400

    def query_announcements(self, boxtype=['news', 'event', ''], uuid=None):
        if self.args['site'] is not None:
            path = self.args['site']
        elif uuid is not None:
            entr = self.zmsindex({'get_uid': 'uid:' + uuid})
            path = len(entr) > 0 and entr[0].getPath() or None
        else:
            entr = self.zmsindex({'get_uid': 'uid:' + self.default_uuid})
            path = len(entr) > 0 and entr[0].getPath() or None

        if path is not None:
            elements = self.zmsindex({'meta_id': self.default_meta, 'path': path})
        else:
            return False

        print(boxtype)
        #elements = self.zmsindex({'meta_id': self.default_meta, 'path': site})
        #foo = self.zmsindex({'get_uid': 'uid:'+self.default_uuid})
        #elements = foo[0].getObject().getChildNodes()
        print("total: {}".format(len(elements)))

        for i, e in enumerate(elements):
            obj = e.getObject()

            # filter out inactive and/or unpublished elements
            active_parent = obj.getParentNode().isActive(REQUEST={'lang': 'ger'}) and 1 or 0
            active_self = obj.attr('active', REQUEST={'lang': 'ger'}) and 1 or 0
            available = obj.attr('attr_active_end', REQUEST={'lang': 'ger'})

            if available is not None:
                available = time.mktime(available) >= time.time() and 1 or 0
            else:
                available = 1

            print(i, active_parent, active_self, obj.attr('boxtype'), available)

            if active_parent and active_self and available and (obj.attr('boxtype') in boxtype):
                try:
                    infolink_de = self.zmscontent.getLinkUrl(obj.attr('attr_url', REQUEST={'lang': 'ger'}))
                    infolink_en = self.zmscontent.getLinkUrl(obj.attr('attr_url', REQUEST={'lang': 'eng'}))
                except:
                    infolink_de = ""
                    infolink_en = ""
                    print(e.getPath())
                img = obj.attr('img')

                protocol = obj.getConfProperty('ASP.protocol', 'http')
                domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
                href = '{}://{}'.format(protocol, domain)

                announcement = {
                    'uuid': e.get_uid.replace('uid:', ''),
                    'path': href + e.getPath(),
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
                        'de': infolink_de,
                        'en': infolink_en
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

                self.announcements.append(announcement)

        print("filtered: {}".format(len(self.announcements)))

        if len(self.announcements) > 0:
            return True
        return False

    def filter_announcements(self):
        # order by eventdate
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
        return filtered_announcements[0:self.default_limit]


class AnnouncementNews(Announcement, Resource):

    def get(self, uuid=None):
        if self.query_announcements(boxtype=['news'], uuid=uuid):
            return jsonify(self.filter_announcements())
        return 'Empty response', 400


class AnnouncementEvents(Announcement, Resource):

    def get(self, uuid=None):
        if self.query_announcements(boxtype=['event'], uuid=uuid):
            return jsonify(self.filter_announcements())
        return 'Empty response', 400


class AnnouncementNodes(Announcement, Resource):

    def __init__(self):
        Announcement.__init__(self)
        self.default_site = '/unibe/portal/'
        self.default_meta = 'newscontainer'
        self.newscontainers = []

    def get(self):
        site = self.args['site'] is not None and self.args['site'] or self.default_site

        print(site)
        elements = self.zmsindex({'meta_id': self.default_meta, 'path': site})
        print("total: {}".format(len(elements)))

        for i, e in enumerate(elements):
            obj = e.getObject()

            # filter out inactive and/or unpublished elements
            active_parent = obj.getParentNode().isActive(REQUEST={'lang': 'ger'}) and 1 or 0
            active_self = obj.attr('active', REQUEST={'lang': 'ger'}) and 1 or 0
            available = obj.attr('attr_active_end', REQUEST={'lang': 'ger'})

            if available is not None:
                available = time.mktime(available) >= time.time() and 1 or 0
            else:
                available = 1

            if '/portal/content/' in e.getPath():
                org_site_de = obj.getParentNode().attr('title', REQUEST={'lang': 'ger'})
                org_site_en = obj.getParentNode().attr('title', REQUEST={'lang': 'eng'})
                org_type = 'Portal'
            else:
                org_site_de = obj.getParentByLevel(0).attr('title', REQUEST={'lang': 'ger'})
                org_site_en = obj.getParentByLevel(0).attr('title', REQUEST={'lang': 'eng'})
                org_type = obj.getParentByLevel(0).attr('attr_dc_type')

            print(i, active_parent, active_self, org_type, org_site_de, available)

            if active_parent and active_self and available:
                protocol = obj.getConfProperty('ASP.protocol', 'http')
                domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
                href = '{}://{}'.format(protocol, domain)

                newscontainer = {
                    'uuid': e.get_uid.replace('uid:', ''),
                    'path': href + e.getPath(),
                    'type': org_type,
                    'site': {
                        'de': org_site_de,
                        'en': org_site_en
                    },
                    'title': {
                        'de': obj.attr('title', REQUEST={'lang': 'ger'}),
                        'en': obj.attr('title', REQUEST={'lang': 'eng'})
                    }
                }
                self.newscontainers.append(newscontainer)

        print("filtered: {}".format(len(self.newscontainers)))

        if len(self.newscontainers) > 0:
            return jsonify(self.newscontainers)
        return 'Empty response', 400
