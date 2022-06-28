FROM ep-devops.id.unibe.ch:5000/id/unibe-cmsbase:python3.10.5-zope5.5.2

ENV ZODB_STORAGE="zeo:8000?storage=main" \
    ACCESS_LOG_DIR="/app/log" \
    ERROR_LOG_DIR="/app/log"

COPY flask-zodb $APPHOME/flask-zodb
COPY zms-headless $APPHOME/zms-headless
COPY requirements-flask.txt $APPHOME/requirements-flask.txt
# COPY constraints-cmsapi.txt $APPHOME/constraints-cmsapi.txt
# TODO: Update and add -c $APPHOME/constraints-cmsapi.txt in release-Branches

RUN $APPHOME/bin/pip install \
    -r $APPHOME/requirements-flask.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.5.2/constraints.txt

COPY cmsapi $APPHOME/cmsapi
COPY init_scripts $ENTRYPOINT_SCRIPTS