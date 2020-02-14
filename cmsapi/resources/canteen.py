from cmsapi.db import zodb
from flask import jsonify
from flask_restful import Resource


class Canteen(Resource):

    def __init__(self):
        print(zodb)
        self.zmscontent = zodb['Application']['unibe']['content']
        self.zmsindex = zodb['Application']['unibe']['zcatalog_index']
        self.default_site = '/unibe/portal/microsites/micro_Mensen/content/e52891/'
        self.default_meta = 'ZMSFolder'
        self.canteens = []

    def get(self):
        print(self.default_meta)
        elements = self.zmsindex({'meta_id': self.default_meta, 'path': self.default_site})
        print("total: {}".format(len(elements)))

        for i, e in enumerate(elements):
            obj = e.getObject()

            info_ob = obj.getChildNodes(meta_types='ZMSTextarea')
            info_de = []
            info_en = []
            for ob in info_ob:
                text = ob.attr('text', REQUEST={'lang': 'ger'})
                if text.strip() != "":
                    info_de.append(ob.attr('text', REQUEST={'lang': 'ger'}))
                text = ob.attr('text', REQUEST={'lang': 'eng'})
                if text.strip() != "":
                    info_en.append(ob.attr('text', REQUEST={'lang': 'eng'}))

            protocol = obj.getConfProperty('ASP.protocol', 'http')
            domain = obj.getConfProperty('ASP.ip_or_domain', 'localhost')
            href = '{}://{}'.format(protocol, domain)

            # get all pictures in gallery of Haus der Universititaet
            if e.get_uid.replace('uid:', '') == '71706e50-45bf-4618-8145-3aaee2440a22':
                img_ob = obj.getTreeNodes(meta_types='ZMSGraphic')
            else:
                img_ob = obj.getChildNodes(meta_types='ZMSGraphic')

            img_de = []
            img_en = []
            for ob in img_ob:
                img = (ob.attr('img') is not None and not isinstance(ob.attr('img'), str)) and href + ob.attr('img').getHref(
                    REQUEST={'lang': 'ger'}) or ''
                if img.strip() != "":
                    img_de.append(img)
                img = (ob.attr('img') is not None and not isinstance(ob.attr('img'), str)) and href + ob.attr('img').getHref(
                    REQUEST={'lang': 'eng'}) or ''
                if img.strip() != "":
                    img_en.append(img)

            canteen = {
                'uuid': e.get_uid.replace('uid:', ''),
                'path': href + e.getPath(),
                'title': {
                    'de': obj.attr('title', REQUEST={'lang': 'ger'}),
                    'en': obj.attr('title', REQUEST={'lang': 'eng'})
                },
                'info': {
                    'de': info_de,
                    'en': info_en
                },
                'image': {
                    'de': img_de,
                    'en': img_en
                },
            }

            self.canteens.append(canteen)

        return jsonify(self.canteens)
