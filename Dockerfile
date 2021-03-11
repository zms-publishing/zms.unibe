FROM ep-devops.id.unibe.ch:5000/id/unibe-cmsbase:python3.9.2-zope5.1.2

COPY requirements-flask.txt $PYTHONPATH/requirements-flask.txt
COPY zms-headless $PYTHONPATH/zms-headless

RUN bin/pip install $PYTHONPATH/zms-headless \
    -r $PYTHONPATH/requirements-flask.txt \
    -c https://zopefoundation.github.io/Zope/releases/5.1.2/constraints.txt \
 && mkdir log

COPY cmsapi $PYTHONPATH/cmsapi

ENV ZODB_STORAGE="zeo:8000?storage=main"

EXPOSE 5000

CMD [ "bin/gunicorn", "cmsapi.app:app", "--bind", "0.0.0.0:5000", \
      "--timeout", "60", \
      "--access-logfile", "log/access.log", \
      "--error-logfile", "log/error.log" ]
