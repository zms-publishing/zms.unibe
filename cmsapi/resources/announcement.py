from flask import jsonify
from flask_restful import Resource, reqparse, inputs

from cmsapi.db import zodb


class Announcement(Resource):

    def __init__(self):
        self.zmscontent = zodb['Application']['myzmsx']['content']
        self.zmsindex = zodb['Application']['myzmsx']['zcatalog_index']

        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('limit', type=int)
        self.parser.add_argument('search', type=str)
        self.parser.add_argument('site', type=str)
        self.parser.add_argument('recursive', type=inputs.boolean)
        self.args = self.parser.parse_args()

        self.announcements = []

    def query_announcements(self, meta_types):
        for i, n in enumerate(self.zmsindex({'meta_id': meta_types})):
            nobj = n.getObject()
            announcement = {
                'uuid': n.get_uid.replace('uid:', ''),
                'type': n.meta_id,
                'path': n.getPath(),
                'title': {
                    'de': nobj.attr('title', REQUEST={'lang': 'ger'}),
                    'en': nobj.attr('title', REQUEST={'lang': 'eng'})
                },
                'description': {
                    'de': nobj.attr('attr_dc_description', REQUEST={'lang': 'ger'}),
                    'en': nobj.attr('attr_dc_description', REQUEST={'lang': 'eng'})
                },
                'active': {
                    'from': {
                        'de': self.zmscontent.getLangFmtDate(
                            nobj.attr('attr_active_start', REQUEST={'lang': 'ger'}),
                            fmt_str='ISO8601'),
                        'en': self.zmscontent.getLangFmtDate(
                            nobj.attr('attr_active_start', REQUEST={'lang': 'eng'}),
                            fmt_str='ISO8601')
                    },
                    'until': {
                        'de': self.zmscontent.getLangFmtDate(
                            nobj.attr('attr_active_end', REQUEST={'lang': 'ger'}),
                            fmt_str='ISO8601'),
                        'en': self.zmscontent.getLangFmtDate(
                            nobj.attr('attr_active_end', REQUEST={'lang': 'eng'}),
                            fmt_str='ISO8601')
                    }
                },
                'created': {
                    'date': {
                        'de': self.zmscontent.getLangFmtDate(
                            nobj.attr('created_dt', REQUEST={'lang': 'ger'}),
                            fmt_str='ISO8601'),
                        'en': self.zmscontent.getLangFmtDate(
                            nobj.attr('created_dt', REQUEST={'lang': 'eng'}),
                            fmt_str='ISO8601')
                    },
                    'user': {
                        'de': nobj.attr('created_uid', REQUEST={'lang': 'ger'}),
                        'en': nobj.attr('created_uid', REQUEST={'lang': 'eng'})
                    }
                }
            }

            # process given site only
            # recursively if set, default is False
            site = self.args['site']
            recursive = self.args['recursive']
            content = '/content/'
            if recursive:
                content = ''
            if site is not None:
                if announcement['path'].lower().find('/' + site.lower() + content) > -1:
                    self.announcements.append(announcement)
            else:
                if announcement['path'].lower().find('/myzmsx' + content) > -1:
                    self.announcements.append(announcement)

    def filter_announcements(self):
        # order by date
        announcements = sorted(self.announcements, key=lambda k: k['active']['from']['de'])
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

    def get(self):
        self.query_announcements(['ZMSFolder', 'ZMSDocument'])
        return jsonify(self.filter_announcements())


class AnnouncementType(Announcement, Resource):

    def get(self, meta_type):
        # TODO: remove temporary type mapping
        meta_type = meta_type == 'news' and 'ZMSDocument' or meta_type == 'events' and 'ZMSFolder' or ''
        self.query_announcements(meta_type)
        return jsonify(self.filter_announcements())
