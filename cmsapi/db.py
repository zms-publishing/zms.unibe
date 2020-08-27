# Flask-ZODB==0.1 (py2 only)
# from flaskext.zodb import ZODB

# Flask-ZODB==0.2dev (py2+p3)
from flask_zodb import ZODB
from flask_sqlalchemy import SQLAlchemy

zodb = ZODB()
sqldb = SQLAlchemy()
