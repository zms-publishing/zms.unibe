FROM ep-devops.id.unibe.ch:5000/id/unibe-cmsbase:python3.10.4-zope5.5.1

ENV ZODB_STORAGE="zeo:8000?storage=main" \
    ACCESS_LOG_DIR="/app/log" \
    ERROR_LOG_DIR="/app/log"

COPY flask-zodb $APPHOME/flask-zodb
COPY zms-headless $APPHOME/zms-headless
COPY requirements-flask.txt $APPHOME/requirements-flask.txt

RUN $APPHOME/bin/pip install \
    -r $APPHOME/requirements-flask.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.5.1/constraints.txt

COPY cmsapi $APPHOME/cmsapi
COPY init_scripts $ENTRYPOINT_SCRIPTS