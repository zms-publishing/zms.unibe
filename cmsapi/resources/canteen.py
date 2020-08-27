import httplib
import re
import ast

from cmsapi.db import zodb
from flask import jsonify
from flask_restful import Resource
from flask_restx import Namespace, fields
from Products.zms import _blobfields

api = Namespace("Canteens", path='/canteens')


@api.route('/<uuid>/', endpoint='canteens_uuid')
class Canteen(Resource):

    def __init__(self):
        self.zmscontent = zodb['Application']['unibe']['portal']['microsites']['micro_Mensen']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_site = '/unibe/portal/microsites/micro_Mensen/content/e52891/'
        self.canteens = []

    def get(self, uuid=None):
        """
        Retrieve details of a canteen from mensa.unibe.ch
        ---
        tags:
            - Canteens
        parameters:
            - name: uuid
              in: path
              required: true
              description: The identifier of the canteen
              type: string
        responses:
            200:
                description: OK
            204:
                description: No canteens found
        """
        if uuid is not None:
            elements = self.zmsindex({'get_uid': 'uid:' + uuid})
            if self.query_canteens(elements):
                return jsonify(self.canteens)
        return '', httplib.NO_CONTENT

    def query_canteens(self, elements=None):
        if elements is not None:
            for i, e in enumerate(elements):
                obj = e.getObject()

                # do not process Haus der Universitaet
                if e.get_uid.replace('uid:', '') == '71706e50-45bf-4618-8145-3aaee2440a22' or \
                        obj.getParentNode() is not None and obj.getParentNode().getId() == 'e52912':
                    continue

                info_ob = obj.filteredChildNodes(meta_types='ZMSTextarea')
                info_de = []
                for ob in info_ob:
                    text = ob.attr('text', REQUEST={'lang': 'ger'})
                    if text.strip() != "":
                        info_de.append(ob.attr('text', REQUEST={'lang': 'ger'}).replace(
                            '&nbsp;', ' ').replace(
                            '<p> </p>', '').replace(
                            '<h3> </h3>', ''))

                protocol = obj.getConfProperty('ASP.protocol', 'http')
                domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
                href = '{}://{}'.format(protocol, domain)

                img_ob = obj.getChildNodes(meta_types='ZMSGraphic')
                img_de = []
                for ob in img_ob:
                    img = (ob.attr('img') is not None and isinstance(ob.attr('img'), _blobfields.MyImage)) and href + \
                          ob.attr('img').getHref(REQUEST={'lang': 'ger'}) or ''
                    if img.strip() != "":
                        img_de.append(img)

                title_de = obj.attr('title', REQUEST={'lang': 'ger'})

                zfv_id = ''
                try:
                    zfv_ids = ast.literal_eval(self.zmscontent.getConfProperty('ZFV.mensa.ids', '{}'))
                    if zfv_ids is not None and len(zfv_ids) > 0:
                        if title_de in zfv_ids:
                            zfv_id = zfv_ids[title_de]
                except ValueError:
                    pass

                canteen = {
                    'uuid': e.get_uid.replace('uid:', ''),
                    'href': href,
                    'path': e.getPath(),
                    'zfvid': zfv_id,
                    'title': {
                        'de': title_de,
                    },
                    'address': {
                        'street': obj.contactmap.attr('streetAddress'),
                        'zipcode': obj.contactmap.attr('postalCode'),
                        'city': obj.contactmap.attr('addressLocality'),
                        'geopos': obj.contactmap.attr('coordValues'),
                    },
                    'info': {
                        'de': [re.sub('(\n|\r)', '', s) for s in info_de],
                    },
                    'image': {
                        'de': img_de,
                    },
                }

                if self.default_site in e.getPath():
                    self.canteens.append(canteen)

        if len(self.canteens) > 0:
            return True
        return False


@api.route('/overview/', endpoint='canteens_overview')
class CanteenOverview(Canteen, Resource):
    def __init__(self):
        self.zmscontent = zodb['Application']['unibe']['portal']['microsites']['micro_Mensen']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_site = '/unibe/portal/microsites/micro_Mensen/content/e52891/'
        self.default_meta = 'ZMSFolder'
        self.canteens = []

    def get(self):
        """
        Retrieve an overview of all canteens from mensa.unibe.ch
        ---
        tags:
            - Canteens
        responses:
            200:
                description: OK
            204:
                description: No canteens found
        """
        elements = self.zmsindex({'meta_id': self.default_meta, 'path': self.default_site})
        print("total: {}".format(len(elements)))

        if self.query_canteens(elements):
            return jsonify(self.canteens)
        return '', httplib.NO_CONTENT
