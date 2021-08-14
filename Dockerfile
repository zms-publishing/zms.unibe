FROM ep-devops.id.unibe.ch:5000/id/unibe-cmsbase:python3.9.6-zope5.3

ENV ZODB_STORAGE="zeo:8000?storage=main" \
    ACCESS_LOG_DIR="/app/log" \
    ERROR_LOG_DIR="/app/log"

COPY requirements-flask.txt $APPHOME/requirements-flask.txt
COPY zms-headless $APPHOME/zms-headless

RUN $APPHOME/bin/pip install $APPHOME/zms-headless \
    -r $APPHOME/requirements-flask.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.3/constraints.txt

COPY cmsapi $APPHOME/cmsapi
COPY init_scripts $ENTRYPOINT_SCRIPTS