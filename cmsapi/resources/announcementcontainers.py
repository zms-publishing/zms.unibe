import httplib
import time

from cmsapi.db import zodb
from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from anytree import Node, RenderTree
from anytree.exporter import JsonExporter, DictExporter
from Products.zms import _blobfields

from cmsapi.resources.announcement import api


@api.route('/containers/', endpoint='announcements_containers')
class AnnouncementContainers(Resource):
    def __init__(self):
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.zmscontent = zodb['Application']['unibe']['portal']['content']
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('getall', type=inputs.boolean)
        self.args = self.parser.parse_args()
        self.newscontainer = {}

    def get(self):
        """
        Retrieve identifiers of containers with news and/or events as hierarchical overview
        ---
        tags:
            - News and Events
        parameters:
            - name: getall
              in: query
              required: false
              description: "Retrieve containers deep in the hierarchy (default mode: only at root level of a subsite)"
              type: boolean
        responses:
            200:
                description: OK
            204:
                description: Empty response
        """
        t0 = time.time()

        # Create a dict of available newscontainers
        self.retrieve_newscontainers('/unibe/portal')
        t1 = time.time()

        # Create a tree of unibe portal clients
        tree = self.traverse_clients(self.zmscontent)
        t2 = time.time()

        # print export_json(tree)
        # print render_tree(tree)
        # print 'AnnouncementContainers.retrieve_newscontainers(): done in %.2fsecs.' % (t1 - t0)
        # print 'AnnouncementContainers.traverse_clients(): done in %.2fsecs.' % (t2 - t1)
        # print 'AnnouncementContainers.get(): done in %.2fsecs.' % (t2 - t0)

        if tree is not None:
            return jsonify([DictExporter(attriter=lambda attrs:[(k, v) for k, v in attrs if k != "name"]).export(tree)])
        return '', httplib.NO_CONTENT

    def retrieve_newscontainers(self, path=''):
        for i, n in enumerate(self.zmsindex({'meta_id': 'newscontainer', 'path': path})):
            n_uuid = n.get_uid.replace('uid:', '')
            n_path = n.getPath()
            n_meta = n.meta_id

            is_at_root_level = len(n_path.split('/content')[1].split('/')) == 2 and True or False
            if not is_at_root_level:
                if self.args['getall'] in [None, False, 0]:
                    continue

            # There may be orphaned entries in ZMSIndex due to tree deleting/moving.
            # Skip these entries by using ZReferableItem.getLinkObj(path)
            # instead of try/except using AbstractCatalogBrain.getObject()
            # because the latter ZCatalog method has a bad performnce in this case.
            if self.zmscontent.getLinkObj('{{${}}}'.format(n_path[1:])) is None:
                # print "Object not found:", n_uuid, n_path
                continue

            n_obj = n.getObject()
            n_href = get_config_domain(n_obj, self.zmscontent)

            if n_obj.isActive(REQUEST={'lang': 'ger'}) and n_obj.getParentNode().isActive(REQUEST={'lang': 'ger'}):
                base_path = n_path.split('/content/')[0] + '/content'
                if base_path not in self.newscontainer.keys():
                    self.newscontainer[base_path] = []

                self.newscontainer[base_path].append({
                    'uuid': n_uuid,
                    'path': n_path,  # Beware: 'path' is a reserved attribute of anytree
                    'type': n_meta,
                    'href': n_href,
                    'title': {
                        'de': n_obj.attr('title', REQUEST={'lang': 'ger'}),
                        'en': n_obj.attr('title', REQUEST={'lang': 'eng'}),
                    }
                })

    def traverse_clients(self, client, parent=None):
        root = None

        if client.isActive(REQUEST={'lang': 'ger'}):
            c_uuid = client._uid  # ZMSIndexZCatalog.get_uid() not available
            c_path = client.absolute_url_path()
            c_meta = client.attr('attr_dc_type')
            c_title = {
                'de': client.attr('title', REQUEST={'lang': 'ger'}),
                'en': client.attr('title', REQUEST={'lang': 'eng'}),
            }
            c_descr = {
                'de': client.attr('attr_dc_description', REQUEST={'lang': 'ger'}).replace('\r', '').replace('\n', ''),
                'en': client.attr('attr_dc_description', REQUEST={'lang': 'eng'}).replace('\r', '').replace('\n', ''),
            }
            c_href = get_config_domain(client, self.zmscontent)

            c_image_de = client.attr('titleimage', REQUEST={'lang': 'ger'})
            c_image_en = client.attr('titleimage', REQUEST={'lang': 'eng'})
            c_image = {
                'de': (c_image_de is not None and isinstance(
                    c_image_de, _blobfields.MyImage)) and c_href + c_image_de.getHref(REQUEST={'lang': 'ger'}) or '',
                'en': (c_image_en is not None and isinstance(
                    c_image_en, _blobfields.MyImage)) and c_href + c_image_en.getHref(REQUEST={'lang': 'eng'}) or ''
            }
            c_address = {
                'street': client.get('contactmap', None) is not None and client.contactmap.attr('streetAddress') or '',
                'zipcode': client.get('contactmap', None) is not None and client.contactmap.attr('postalCode') or '',
                'city': client.get('contactmap', None) is not None and client.contactmap.attr('addressLocality') or '',
                'geopos': client.get('contactmap', None) is not None and client.contactmap.attr('coordValues') or '',
            }

            # Set client with its data as tree node
            if parent is None:
                node = Node(c_uuid,
                            uuid=c_uuid,
                            path=c_path,  # Beware: 'path' is a reserved attribute of anytree
                            title=c_title,
                            type=c_meta,
                            description=c_descr,
                            href=c_href,
                            image=c_image,
                            address=c_address,
                            announcements=[])
                root = node
            else:
                node = Node(c_uuid, parent=parent,
                            uuid=c_uuid,
                            path=c_path,  # Beware: 'path' is a reserved attribute of anytree
                            title=c_title,
                            type=c_meta,
                            description=c_descr,
                            href=c_href,
                            image=c_image,
                            address=c_address,
                            announcements=[])

            # Assign the corresponding newscontainers to the client
            if c_path in self.newscontainer.keys():
                node.announcements = self.newscontainer[c_path]

            # Traverse clients recursively
            for client in client.getPortalClients():
                if client.isActive(REQUEST={'lang': 'ger'}):
                    self.traverse_clients(client, node)

        return root


def get_config_domain(obj, root):
    protocol = obj.getConfProperty('ASP.protocol', root.getConfProperty('ASP.protocol', 'http'))
    domain = obj.getConfProperty('ASP.ip_or_domain', root.getConfProperty('ASP.ip_or_domain', None))
    if domain is not None:
        return '{}://{}'.format(protocol, domain)
    return ''


def render_tree(tree):
    printed = []
    for pre, fill, node in RenderTree(tree):
        title_de = node.title['de'].decode('utf-8')
        title_en = node.title['en'].decode('utf-8')
        title = title_de == "" and title_en or title_de
        announcements = len(node.announcements) > 0 and "* " or ""
        printed.append("%s%s%s" % (pre, announcements, title))
    return '\n'.join(printed)


def export_json(tree):
    jsonexporter = JsonExporter(indent=2, sort_keys=True, ensure_ascii=False)
    return jsonexporter.export(tree)
