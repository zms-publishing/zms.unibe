import os
import requests

from flask import Flask
from flask_restful import Api, reqparse
from flasgger import Swagger
from flask_jwt_extended import JWTManager

from cmsapi.cache import cache
from cmsapi.db import zodb, sqldb
from cmsapi.resources.announcementagenda import AnnouncementAgenda
from cmsapi.resources.announcementcontainers import AnnouncementContainers
from cmsapi.resources.announcement import Announcement, AnnouncementNews, AnnouncementEvents
from cmsapi.resources.canteen import Canteen, CanteenOverview
from cmsapi.resources.servicelinks import ServiceLinks, ServiceLinksItem

app = Flask(__name__)
app.config["ZODB_STORAGE"] = 'zeo://' + os.getenv('ZODB_STORAGE', '127.0.0.1:8000?storage=main')

cmsapi_version = "2.0.0dev"

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": "cmsapi",
            "route": "/cmsapi.json",  # WORKAROUND
                                      # see ./templates/flasgger/swagger.html
                                      # to get a relative url to be used in non-root deployments
                                      # instead of the absolute url which Flasgger desires by raising
                                      # ValueError: urls must start with a leading slash
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "specs_route": "/",
    "static_url_path": "/",
    "basePath": os.getenv('SWAGGER_BASE_PATH', ''),

    # WORKAROUND
    # for https://github.com/flasgger/flasgger/issues/234
    # to get working links to the resources, which are referenced externally
    "swagger_ui_css": "//unpkg.com/swagger-ui-dist@3.23.4/swagger-ui.css",
    "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@3.23.4/swagger-ui-bundle.js",
    "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@3.23.4/swagger-ui-standalone-preset.js",
    "jquery_js": "//unpkg.com/jquery@2.2.4/dist/jquery.min.js",
    "favicon": "//unpkg.com/swagger-ui-dist@3.23.4/favicon-32x32.png",

    "swagger_ui": True,
    "hide_top_bar": True,
    "ui_params": {
        "displayRequestDuration": True,
        "supportedSubmitMethods": "get",
    },
    "docExpansion": "list",
    "title": "CMSAPI v{}".format(cmsapi_version),
}

swagger_template = {
    "info": {
        "title": "CMSAPI",
        "version": cmsapi_version,
        "description": "REST-API to connect with UniBE CMS",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "",
            "url": "",
        },
        "termsOfService": "",
    },
}

zodb.init_app(app)
cache.init_app(app)
jwt = JWTManager(app)
api = Api(app, prefix='/v{}'.format(cmsapi_version.split('.')[0]))
swa = Swagger(app, config=swagger_config, template=swagger_template)

api.add_resource(Announcement, '/announcements/<string:uuid>/')
api.add_resource(AnnouncementNews, '/announcements/news/<string:uuid>/')
api.add_resource(AnnouncementEvents, '/announcements/events/<string:uuid>/')
api.add_resource(AnnouncementContainers, '/announcements/containers/')
api.add_resource(AnnouncementAgenda, '/announcements/agenda/')

api.add_resource(Canteen, '/canteens/<string:uuid>/')
api.add_resource(CanteenOverview, '/canteens/overview/')

api.add_resource(ServiceLinks, '/servicelinks/')
api.add_resource(ServiceLinksItem, '/servicelinks/<string:item>/')


@app.route('/healthcheck')
def check_health():
    return "OK", 200


@app.route('/cache/<mode>')
def purge_cache(mode=None):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('key', type=str)
    cache_key = parser.parse_args()['key']  # e.g. '/v2/canteens/overview/'
    if mode == 'purge':
        if cache_key is not None:
            if cache.delete('view/' + cache_key):
                print('cache/delete:', cache_key)
                return "Cache purged for " + cache_key, 200
    if mode == 'refresh':
        if cache_key is not None:
            cache.delete('view/' + cache_key)
            CACHE_REFRESH = os.getenv('CACHE_REFRESH', 'http://127.0.0.1:5000')
            refresh = requests.get(CACHE_REFRESH + cache_key, timeout=60)
            print('cache/refresh:', CACHE_REFRESH + cache_key, refresh.status_code)
            if refresh.status_code in [200, 204]:
                return "Cache refreshed for " + cache_key, 200
            else:
                return "Cache refresh failed for " + cache_key, 404
    if mode == 'purgeall':
        cache.clear()
        print('cache/delete:', cache_key)
        return "Cache purged completely", 200
    return "No cache found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
