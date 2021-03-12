FROM ep-devops.id.unibe.ch:5000/id/unibe-cmsbase:python3.9.2-zope5.1.2

ENV ZODB_STORAGE="zeo:8000?storage=main" \
    ACCESS_LOG_DIR="/app/log" \
    ERROR_LOG_DIR="/app/log" \
    CREATE_USER=false

COPY requirements-flask.txt $APPHOME/requirements-flask.txt
COPY zms-headless $APPHOME/zms-headless
COPY cmsapi $APPHOME/cmsapi
COPY init_scripts $ENTRYPOINT_SCRIPTS

RUN $APPHOME/bin/pip install $APPHOME/zms-headless \
    -r $APPHOME/requirements-flask.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.1.2/constraints.txt