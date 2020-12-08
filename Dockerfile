FROM python:3.6.9-alpine

RUN apk --update upgrade && \
    apk --no-cache add \
        gcc \
        git \
        libffi-dev \
        musl-dev \
        python3-dev && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

ENV INSTALL_PATH=/unibe-cmsapi \
    PYTHONPATH=/unibe-cmsapi \
    ZODB_STORAGE=zeo:8000

COPY . $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN python3 -m venv $INSTALL_PATH \
 && bin/pip install -U pip wheel setuptools \
 && bin/pip install Zope[wsgi]==5.1 \
    -c https://zopefoundation.github.io/Zope/releases/5.1/constraints.txt \
    -e zms-headless

RUN bin/pip install -r requirements-flask.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.1/constraints.txt \
 && mkdir log

EXPOSE 5000

CMD [ "bin/gunicorn", "cmsapi.app:app", "--bind", "0.0.0.0:5000", \
      "--timeout", "60", \
      "--access-logfile", "log/access.log", \
      "--error-logfile", "log/error.log" ]
