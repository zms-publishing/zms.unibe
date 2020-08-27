import httplib
import time

from cmsapi.db import zodb
from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from Products.zms import _blobfields

from cmsapi.resources.announcement import api


@api.route('/overview/', endpoint='announcements_overview')
class AnnouncementOverview(Resource):

    def __init__(self):
        self.zmscontent = zodb['Application']['unibe']['portal']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_meta = 'ZMS'
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('getall', type=inputs.boolean)
        self.args = self.parser.parse_args()

    def get(self):
        """
        Retrieve identifiers of newscontainers containing news and/or events
        ---
        tags:
            - News and Events
        parameters:
            - name: getall
              in: query
              required: false
              description: "Retrieve identifiers of newscontainers of all subsites recursively (default mode: at each root level only)"
              type: boolean
        responses:
            200:
                description: OK
            204:
                description: Empty response
        deprecated:
            true
        """
        if self.args['getall'] in [True, 1]:
            getall = True
        else:
            getall = False

        subsites = [('/unibe/portal/content', '/unibe/portal/content')]

        def get_subsites(subsite):
            active = subsite.isActive(REQUEST={'lang': 'ger'}) or \
                     subsite.isActive(REQUEST={'lang': 'eng'}) and True or False
            if active:
                path = subsite.getPhysicalPath()
                if path[-2] != path[-3] != 'unibe' != 'id':
                    child_path = '/' + subsite.absolute_url()
                    parent_path = '/' + subsite.absolute_url().replace('/' + path[-2], '')
                    subsites.append((child_path, parent_path))
                for subsite in subsite.getPortalClients():
                    get_subsites(subsite)
        get_subsites(self.zmscontent)

        nodes = {}
        for subsite in subsites:
            child_path, parent_path = subsite

            e = self.zmsindex({'meta_id': self.default_meta,
                               'path': child_path})
            if len(e) == 1:
                e = e[0]
                obj = e.getObject()
            else:
                continue

            newscontainers = []
            for n in self.zmsindex({'meta_id': 'newscontainer', 'path': child_path}):
                try:
                    nobj = n.getObject()
                except AttributeError:
                    print("NotFound: " + n.getPath())
                    continue
                path = n.getPath()
                uuid = n.get_uid.replace('uid:', '')

                # filter out inactive and/or unpublished elements
                active_parent = nobj.getParentNode().isActive(REQUEST={'lang': 'ger'}) and True or False
                active_self = nobj.attr('active', REQUEST={'lang': 'ger'}) and True or False
                available = nobj.attr('attr_active_end', REQUEST={'lang': 'ger'})

                if available is not None:
                    available = time.mktime(available) >= time.time() and True or False
                else:
                    available = True

                if active_parent and active_self and available:
                    protocol = nobj.getConfProperty('ASP.protocol', 'http')
                    domain = nobj.getConfProperty('ASP.ip_or_domain', 'localhost')
                    href = '{}://{}'.format(protocol, domain)

                    newscontainer = {
                        'uuid': uuid,
                        'href': href,
                        'path': path,
                        'title': {
                            'de': nobj.attr('title', REQUEST={'lang': 'ger'}),
                            'en': nobj.attr('title', REQUEST={'lang': 'eng'})
                        },
                        'type': nobj.meta_id
                    }

                    root_level = len(path.split('/content')[1].split('/')) == 2 and True or False
                    if not getall:
                        if root_level:
                            newscontainers.append(newscontainer)
                    else:
                        newscontainers.append(newscontainer)

            protocol = obj.getConfProperty('ASP.protocol', 'http')
            domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
            href = '{}://{}'.format(protocol, domain)

            titleimage = obj.attr('titleimage')

            nodes[child_path] = {
                'uuid': e.get_uid.replace('uid:', ''),
                'href': href,
                'path': e.getPath(),
                'title': {
                    'de': obj.attr('title', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('title', REQUEST={'lang': 'eng'}),
                },
                'description': {
                    'de': obj.attr('attr_dc_description', REQUEST={'lang': 'ger'}).replace('\r', '').replace('\n', ''),
                    'en': obj.attr('attr_dc_description', REQUEST={'lang': 'eng'}).replace('\r', '').replace('\n', ''),
                },
                'image': {
                    'de': (titleimage is not None and isinstance(titleimage, _blobfields.MyImage)) and href +
                          obj.attr('titleimage').getHref(REQUEST={'lang': 'ger'}) or '',
                    'en': (titleimage is not None and isinstance(titleimage, _blobfields.MyImage)) and href +
                          obj.attr('titleimage').getHref(REQUEST={'lang': 'eng'}) or ''
                },
                'type': obj.attr('attr_dc_type'),
                'address': {
                    'street': obj.get('contactmap', None) is not None and
                              obj.contactmap.attr('streetAddress') or '',
                    'zipcode': obj.get('contactmap', None) is not None and
                               obj.contactmap.attr('postalCode') or '',
                    'city': obj.get('contactmap', None) is not None and
                            obj.contactmap.attr('addressLocality') or '',
                    'geopos': obj.get('contactmap', None) is not None and
                              obj.contactmap.attr('coordValues') or '',
                },
                'announcements': newscontainers,
            }

        sitemap = []
        for subsite in subsites:
            child_path, parent_path = subsite
            node = nodes.get(child_path, None)
            if child_path == parent_path:
                if node is not None:
                    sitemap.append(node)
                else:
                    print("Redirected: " + child_path)
            else:
                parent = nodes[parent_path]
                if 'subsites' not in parent:
                    parent['subsites'] = []
                children = parent['subsites']
                if node is not None:
                    children.append(node)
                else:
                    print("Redirected: " + child_path)

        if len(sitemap) > 0:
            return jsonify(sitemap)
        return '', httplib.NO_CONTENT
