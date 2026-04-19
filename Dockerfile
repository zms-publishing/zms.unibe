# Customize zms-base image version to support local builds
ARG ZMS_BASE_VERSION=python3.13.5-zope5.13

FROM ghcr.io/idasm-unibe-ch/zms-base:$ZMS_BASE_VERSION

ENV ZODB_STORAGE="zeo:8000?storage=main" \
    ACCESS_LOG_DIR="/app/zope/log" \
    ERROR_LOG_DIR="/app/zope/log"

RUN apk update \
 && apk --no-cache add \
    libpq-dev \
    curl

# Install supercronic
# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.26/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=7a79496cf8ad899b99a719355d4db27422396735

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# We use relative copy commands because WORKDIR is set to $APP_HOME in zms-base image
COPY --chown=$USERNAME:$GROUPNAME zms-core zms-core
COPY --chown=$USERNAME:$GROUPNAME zms-addons zms-addons

# TODO: Add pyproject.toml and switch PEP 420 native namespace https://github.com/idasm-unibe-ch/zms-base/issues/3
RUN $VENV_HOME/bin/pip install ./zms-core --use-pep517 --config-settings editable_mode=compat \
    -e ./'zms-addons[fastapi]' \
    -c ./zms-addons/constraints.txt \
    -c https://zopefoundation.github.io/Zope/releases/$ZOPE_VERSION/constraints.txt

COPY --chown=$USERNAME:$GROUPNAME cmsapi cmsapi
COPY --chown=$USERNAME:$GROUPNAME cron/afterwork /etc/periodic/afterwork
COPY --chown=$USERNAME:$GROUPNAME cron/officehours /etc/periodic/officehours
COPY --chown=$USERNAME:$GROUPNAME cron/weekly /etc/periodic/weekly
COPY --chown=$USERNAME:$GROUPNAME init_scripts $ENTRYPOINT_SCRIPTS

# Run with restricted user
USER $USERNAME
