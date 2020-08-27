FROM python:2.7-alpine

RUN apk --update upgrade && \
    apk --no-cache add \
        gcc \
        git \
        libffi-dev \
        musl-dev \
        python2-dev && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

# für die Image-Grösse ist das seit einigen Versionen irrelevant, aber man spart sich einen
# intermediate container, so dass sich die Build-Zeit verkürzt
ENV INSTALL_PATH=/restapi \
    PYTHONPATH=/restapi \
    ZODB_STORAGE=zeo://host.docker.internal:9027

# TODO: run as user zope instead of root

RUN pip install virtualenv && \
    virtualenv $INSTALL_PATH

# COPY in einem Aufruf, so dass Build-Time geringer. Ich hoffe, das funktioniert mit dem pip install /danach/
COPY cmsapi /$INSTALL_PATH/cmsapi
#ADD zms3-headless.tar.gz zms3-headless injected by git submodule
COPY zms3-headless /$INSTALL_PATH/zms3-headless
COPY requirements-zms3.txt \
    requirements-flask.txt \
    /$INSTALL_PATH/

WORKDIR $INSTALL_PATH

RUN bin/pip install -U pip \
 && bin/pip install -r requirements-zms3.txt \
 && bin/pip install -r requirements-flask.txt \
 && mkdir log

EXPOSE 5000
CMD [ "bin/gunicorn", "cmsapi.app:app", "--bind", "0.0.0.0:5000", \
      "--timeout", "60", \
      "--access-logfile", "log/access.log", \
      "--error-logfile", "log/error.log" ]
