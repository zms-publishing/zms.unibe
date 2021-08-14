import http

from cmsapi.cache import cache
from cmsapi.db import zodb
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_restx import Namespace
from Products.zms import _blobfields

api = Namespace("Service Links", path='/servicelinks')


@api.route('/', endpoint='servicelinks')
class ServiceLinks(Resource):

    def __init__(self):
        # map possible endpoints to ZMS content UID in client "Uni App"
        self.possible_items = {
            'contact': '58115e60-e80b-44c1-9a7d-bc65a42c9d5a',
            'imprint': 'd15e37f5-b317-4b47-baf1-c203a34bd0ad',
            'indexaz': '27bfdd98-c79b-4dd4-b69a-dd1bde958d0b',
            'locations': '1c0a8927-bfb4-4215-a8fd-c41bba079d21',
            'privacypolicy': 'a7f29281-43e0-4607-871b-39e66204bb31',
            'termsofservice': '4b570198-0485-4f75-8242-9e5a7528351a'
        }

    def get(self):
        """
        Returns possible values for an {item} to be retrieved
        ---
        tags:
            - Service Links
        responses:
            200:
                description: OK
            204:
                description: No information found
        """
        return jsonify({'servicelinks_items': sorted(self.possible_items.keys())})


@api.route('/<item>/', endpoint='servicelinks_item')
class ServiceLinksItem(ServiceLinks, Resource):

    def __init__(self):
        super(ServiceLinksItem, self).__init__()
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.zmscontent = zodb['Application']['unibe']['uniapp']['content']
        self.zmssite = '/unibe/uniapp/content/'
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.args = self.parser.parse_args()

    @cache.cached()
    def get(self, item=None):
        """
        Retrieve information from the requested item
        ---
        tags:
            - Service Links
        parameters:
            - name: item
              in: path
              required: true
              description: A possible value taken from /servicelinks
              type: string
        responses:
            200:
                description: OK
            204:
                description: No information found
        """
        if item in self.possible_items:
            # map attributes and languages to be retrieved from ZMS to keys in JSON output
            attrs = {
                'title': 'title',
                'text': 'text',
                'attr_dc_description': 'meta',
                'attr_ref': 'href',  # disabled acquisition of ZMSLinkElement-3.1.28 to set multilingual=true
                                     # in client "Uni App" - obscure why this is not default in UniBE master
                'file': 'href',
                'change_dt': 'lastmodified',
            }
            langs = {
                'ger': 'de',
                'eng': 'en',
            }
            service_items = []
            elements = self.zmsindex({'get_uid': 'uid:' + self.possible_items[item]})

            if elements is not None:
                for i, e in enumerate(elements):
                    for obj in e.getObject().filteredChildNodes(meta_types=[
                        'ZMSTextarea',
                        'ZMSLinkElement',
                        'filecontainer',
                    ]):
                        service_item = {}

                        # get values of defined attrs in defined langs
                        for lang in langs.keys():
                            for attr in attrs.keys():
                                value = get_value(obj, attr, lang)
                                if value is not None:
                                    if attrs[attr] not in service_item:
                                        service_item[attrs[attr]] = {}
                                    service_item[attrs[attr]][langs[lang]] = value

                        # get location data files organized in filecontainers
                        if obj.meta_id == 'filecontainer':
                            service_item['files'] = []
                            for file_obj in obj.filteredChildNodes(meta_types=['ZMSFile']):
                                for lang in langs.keys():
                                    href = get_value(file_obj, 'file', lang)
                                    if href is not None:
                                        meta = get_value(file_obj, 'attr_dc_description', lang)
                                        lastmodified = get_value(file_obj, 'change_dt', lang)
                                        if meta is not None:
                                            service_item['files'].append({
                                                'href': {langs[lang]: href},
                                                'lastmodified': {langs[lang]: lastmodified},
                                                'meta': {langs[lang]: meta},
                                            })
                                        else:
                                            service_item['files'].append({
                                                'href': {langs[lang]: href},
                                                'lastmodified': {langs[lang]: lastmodified},
                                            })

                        service_items.append(service_item)

            return jsonify(service_items)
        return '', http.HTTPStatus.NO_CONTENT


def get_value(obj, attr, lang):
    req = {'lang': lang}
    if obj.isVisible(REQUEST=req):
        value = obj.attr(attr, REQUEST=req)
        if attr in ['title', 'titlealt', 'text']:
            value = value.replace('&nbsp;', ' ').replace('\r', '').replace('\n', '')
        if attr in ['file', 'img']:
            protocol = obj.getConfProperty('ASP.protocol', 'http')
            domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
            url = '{}://{}'.format(protocol, domain)
            if isinstance(value, _blobfields.MyFile) or isinstance(value, _blobfields.MyImage):
                value = url + value.getHref(REQUEST=req)
        if attr in ['attr_ref']:
            linkobj = obj.getLinkObj(value)
            portalmaster = obj.breadcrumbs_obj_path(True)[0]
            if linkobj is not None and portalmaster is not None:
                url = linkobj.getHref2IndexHtml(REQUEST=req)
                value = linkobj.getHref2IndexHtmlInContext(portalmaster, url, REQUEST=req)
        if attr in ['created_dt', 'change_dt', 'attr_active_start', 'attr_active_end']:
            value = obj.getLangFmtDate(value, fmt_str='ISO8601')
        if value.strip() != '':
            return value
    return None
