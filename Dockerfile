FROM python:3.7-alpine

RUN apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    python3-dev \
    git

ENV INSTALL_PATH /restapi

# TODO run as user zope instead of root

RUN python3.7 -m venv $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN bin/pip install -U pip \
 && bin/pip install -r https://zopefoundation.github.io/Zope/releases/4.1.3/requirements-full.txt

# $ cd /Users/cm19b120/Workspace/UniBE/Flask/zms4
# $ git archive --output /Users/cm19b120/Workspace/UniBE/Flask/unibe-cms/restapi/zms4-headless.tar.gz zms-headless
ADD zms4-headless.tar.gz zms4-headless
COPY requirements.txt requirements.txt

RUN bin/pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["bin/python", "cmsapi/app.py"]
