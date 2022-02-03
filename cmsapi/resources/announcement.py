import http
import time
import urllib

from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from flask_restx import Namespace, fields
from Products.zms import _blobfields

from cmsapi.cache import cache
from cmsapi.db import zodb

api = Namespace("News and Events", path='/announcements')


@api.route('/<uuid>/', endpoint='announcements_uuid')
class Announcement(Resource):

    def __init__(self):
        self.zmscontent = zodb['Application']['unibe']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_path = '/unibe/portal/content/e299592'
        self.default_uuid = '271a321e-993e-4e36-b9a1-5b1f1d35e7f5'
        self.default_meta = 'newsbox'
        #self.default_limit = 50
        self.announcements = []

        self.parser = reqparse.RequestParser(bundle_errors=True)
        #self.parser.add_argument('limit', type=int)
        #self.parser.add_argument('search', type=str)
        self.parser.add_argument('path', type=str)
        self.parser.add_argument('created', type=str)
        self.parser.add_argument('changed', type=str)
        #self.parser.add_argument('recursive', type=inputs.boolean)
        self.args = self.parser.parse_args()

    @cache.cached()
    def get(self, uuid=None):
        """
        Retrieve all news/events of the specified identifier
        ---
        tags:
            - News and Events
        parameters:
            - name: uuid
              in: path
              required: true
              description: The identifier of the newscontainer taken from /announcements/containers
              type: string
            - name: created
              in: query
              required: false
              description: "Filter by given creation date as starting point (format: YYYY[MM[DD]] / default: 1 year ago)"
              type: date
            - name: changed
              in: query
              required: false
              description: "Filter by given modification date as starting point (format: YYYY[MM[DD]] / default: 1 year ago)"
              type: date
        responses:
            200:
                description: OK
            204:
                description: No news/events found
        """
        print("### not cached Announcement.get", uuid)
        if self.query_announcements(uuid=uuid):
            return jsonify(self.filter_announcements())
        return '', http.HTTPStatus.NO_CONTENT

    def query_announcements(self, boxtype=None, uuid=None):
        if boxtype is None:
            boxtype = ['news', 'event', '']
            
        if self.args['path'] is not None:
            path = urllib.unquote_plus(self.args['path'])
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

        # if no created/changed dates are given
        # default time span: one year ago
        default_timespan = 31536000

        created_filter = self.args['created']
        created_ft = time.time() - default_timespan
        if created_filter is not None and created_filter.isdigit():
            try:
                if len(created_filter) == 4:
                    created_ft = time.mktime(time.strptime(created_filter, '%Y'))
                elif len(created_filter) == 6:
                    created_ft = time.mktime(time.strptime(created_filter, '%Y%m'))
                elif len(created_filter) == 8:
                    created_ft = time.mktime(time.strptime(created_filter, '%Y%m%d'))
            except ValueError:
                return False

        changed_filter = self.args['changed']
        changed_ft = time.time() - default_timespan
        if changed_filter is not None and changed_filter.isdigit():
            try:
                if len(changed_filter) == 4:
                    changed_ft = time.mktime(time.strptime(changed_filter, '%Y'))
                elif len(changed_filter) == 6:
                    changed_ft = time.mktime(time.strptime(changed_filter, '%Y%m'))
                elif len(changed_filter) == 8:
                    changed_ft = time.mktime(time.strptime(changed_filter, '%Y%m%d'))
            except ValueError:
                return False

        for i, e in enumerate(elements):
            obj = e.getObject()

            # filter out inactive and/or unpublished elements by default
            # filter out elements by created/changed date query parameter
            active_parent = obj.getParentNode().isActive(REQUEST={'lang': 'ger'}) and True or False
            active_self = obj.attr('active', REQUEST={'lang': 'ger'}) and True or False
            available = obj.attr('attr_active_end', REQUEST={'lang': 'ger'})
            created_dt = obj.attr('created_dt', REQUEST={'lang': 'ger'})
            changed_dt = obj.attr('change_dt', REQUEST={'lang': 'ger'})

            if available is not None:
                available = time.mktime(available) >= time.time() and True or False
            else:
                available = True

            if created_dt is not None and isinstance(created_dt, time.struct_time):
                created_ok = time.mktime(created_dt) >= created_ft and True or False
            else:
                created_ok = True
                created_dt = time.localtime(time.time() - default_timespan)

            if changed_dt is not None and isinstance(changed_dt, time.struct_time):
                changed_ok = time.mktime(changed_dt) >= changed_ft and True or False
            else:
                changed_ok = True
                changed_dt = time.localtime(time.time() - default_timespan)

            if active_parent and active_self and available \
                    and (created_ok and changed_ok) \
                    and (obj.attr('boxtype') in boxtype):
                try:
                    infolink_de = self.zmscontent.getLinkUrl(obj.attr('attr_url', REQUEST={'lang': 'ger'}))
                    infolink_en = self.zmscontent.getLinkUrl(obj.attr('attr_url', REQUEST={'lang': 'eng'}))
                except:
                    infolink_de = ""
                    infolink_en = ""
                    print('ERROR: Broken Link at ' + e.getPath())
                img = obj.attr('img')

                protocol = 'https'
                domain = obj.getConfProperty('ASP.ip_or_domain', 'www.unibe.ch')
                href = '{}://{}'.format(protocol, domain.replace('cmstest1.', ''))

                text_de = obj.attr('text', REQUEST={'lang': 'ger'}).replace('\r\n', '<br />')
                text_en = obj.attr('text', REQUEST={'lang': 'eng'}).replace('\r\n', '<br />')

                announcement = {
                    'uuid': e.get_uid.replace('uid:', ''),
                    'href': href,
                    'path': e.getPath(),
                    'type': obj.attr('boxtype'),
                    'title': {
                        'de': obj.attr('title', REQUEST={'lang': 'ger'}),
                        'en': obj.attr('title', REQUEST={'lang': 'eng'})
                    },
                    'text': {
                        'de': text_de.replace('\r', '').replace('\n', ''),
                        'en': text_en.replace('\r', '').replace('\n', '')
                    },
                    'image': {
                        'de': (img is not None and isinstance(img, _blobfields.MyImage)) and href +
                              obj.attr('img').getHref(REQUEST={'lang': 'ger'}) or '',
                        'en': (img is not None and isinstance(img, _blobfields.MyImage)) and href +
                              obj.attr('img').getHref(REQUEST={'lang': 'eng'}) or ''
                    },
                    'infolink': {
                        'de': infolink_de.replace('http://', 'https://').replace('cmstest1.', ''),
                        'en': infolink_en.replace('http://', 'https://').replace('cmstest1.', '')
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
                    },
                    'lastmodified': {
                        'created': self.zmscontent.getLangFmtDate(
                                obj.attr('created_dt', REQUEST={'lang': 'ger'}),
                                fmt_str='ISO8601'),
                        'changed': self.zmscontent.getLangFmtDate(
                                obj.attr('change_dt', REQUEST={'lang': 'ger'}),
                                fmt_str='ISO8601'),
                    }
                }
                # show corona news on top by setting the current date
                if '.unibe.ch/coronavirus' in infolink_de and announcement['eventdate']['de'] == 'None':
                    now = time.localtime()
                    announcement['lastmodified'] = {
                        'created': self.zmscontent.getLangFmtDate(
                                now,
                                fmt_str='ISO8601'),
                        'changed': self.zmscontent.getLangFmtDate(
                                now,
                                fmt_str='ISO8601'),
                    }
                self.announcements.append(announcement)

        if len(self.announcements) > 0:
            return True
        return False

    def filter_announcements(self):
        # order by eventdate
        announcements = sorted(self.announcements, key=lambda k: k['eventdate']['de'], reverse=True)
        """
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
        """
        return announcements


@api.route('/news/<uuid>/', endpoint='news_uuid')
class AnnouncementNews(Announcement, Resource):

    @cache.cached()
    def get(self, uuid=None):
        """
        Retrieve only news of the specified identifier
        ---
        tags:
            - News and Events
        parameters:
            - name: uuid
              in: path
              required: true
              description: The identifier of the newscontainer taken from /announcements/containers
              type: string
            - name: created
              in: query
              required: false
              description: "Filter by given creation date as starting point (format: YYYY[MM[DD]] / default: 1 year ago)"
              type: date
            - name: changed
              in: query
              required: false
              description: "Filter by given modification date as starting point (format: YYYY[MM[DD]] / default: 1 year ago)"
              type: date
        responses:
            200:
                description: OK
            204:
                description: No news found
        """
        if self.query_announcements(boxtype=['news'], uuid=uuid):
            return jsonify(self.filter_announcements())
        return '', http.HTTPStatus.NO_CONTENT


@api.route('/events/<uuid>/', endpoint='events_uuid')
class AnnouncementEvents(Announcement, Resource):

    @cache.cached()
    def get(self, uuid=None):
        """
        Retrieve only events of the specified identifier
        ---
        tags:
            - News and Events
        parameters:
            - name: uuid
              in: path
              required: true
              description: The identifier of the newscontainer taken from /announcements/containers
              type: string
            - name: created
              in: query
              required: false
              description: "Filter by given creation date as starting point (format: YYYY[MM[DD]] / default: 1 year ago)"
              type: date
            - name: changed
              in: query
              required: false
              description: "Filter by given modification date as starting point (format: YYYY[MM[DD]] / default: 1 year ago)"
              type: date
        responses:
            200:
                description: OK
            204:
                description: No events found
        """
        if self.query_announcements(boxtype=['event'], uuid=uuid):
            return jsonify(self.filter_announcements())
        return '', http.HTTPStatus.NO_CONTENT
