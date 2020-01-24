FROM python:3.7-alpine

RUN apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    python3-dev \
    openssh \
    git

ENV INSTALL_PATH /restapi

# TODO run as user zope instead of root

RUN python3.7 -m venv $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN bin/pip install -U pip \
 && bin/pip install -r https://zopefoundation.github.io/Zope/releases/4.1.3/requirements-full.txt

COPY . .

# $ cd /Users/cm19b120/Workspace/UniBE/Flask/zms4
# $ git archive --format zip --output /Users/cm19b120/Workspace/UniBE/Flask/unibe-cms/restapi/zms4-headless.zip zms-headless
RUN mkdir zms4-headless \
 && unzip zms4-headless.zip -d zms4-headless \
 && bin/pip install -r requirements.txt

# && bin/pip install -e ./zms4-headless.zip
# ERROR: ./zms4-headless.zip is not a valid editable requirement. It should either be a path to a local project or a VCS URL (beginning with svn+, git+, hg+, or bzr+).
# ERROR: Service 'zms-headless-interface' failed to build: The command '/bin/sh -c bin/pip install -r requirements.txt   && bin/pip install -e ./zms4-headless.zip' returned a non-zero code: 1

EXPOSE 5000

ENTRYPOINT ["bin/python", "cmsapi/app.py"]