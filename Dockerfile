FROM ep-devops.id.unibe.ch:5000/id/unibe-cms-base:python3.10.5-zope5.5.2

ENV ZODB_STORAGE="zeo:8000?storage=main" \
    ACCESS_LOG_DIR="/app/log" \
    ERROR_LOG_DIR="/app/log"

COPY flask-zodb $APPHOME/flask-zodb
COPY zms-headless $APPHOME/zms-headless
COPY frontend/ZMSModels $APPHOME/frontend/ZMSModels
COPY requirements-flask.txt $APPHOME/requirements-flask.txt
COPY requirements-fastapi.txt $APPHOME/requirements-fastapi.txt
COPY constraints-flask.txt $APPHOME/constraints-flask.txt
COPY constraints-fastapi.txt $APPHOME/constraints-fastapi.txt

RUN $APPHOME/bin/pip install \
    -r $APPHOME/requirements-flask.txt \
    -r $APPHOME/requirements-fastapi.txt \
    -c $APPHOME/constraints-flask.txt \
    -c $APPHOME/constraints-fastapi.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.5.2/constraints.txt

COPY cmsapi $APPHOME/cmsapi
COPY init_scripts $ENTRYPOINT_SCRIPTS