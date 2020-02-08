from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from cmsapi.db import zodb, sqldb
from cmsapi.resources.announcement import Announcement, AnnouncementType

app = Flask(__name__)
app.config["ZODB_STORAGE"] = "zeo://localhost:9200"  # zeo://host.docker.internal:9300 zeo://zeo-zodb-storage:9100
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)
jwt = JWTManager(app)

zodb.init_app(app)
sqldb.init_app(app)

api.add_resource(Announcement, '/v0/announcements/')
api.add_resource(AnnouncementType, '/v0/announcements/<string:boxtype>/')


@app.before_first_request
def create_tables():
    sqldb.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
