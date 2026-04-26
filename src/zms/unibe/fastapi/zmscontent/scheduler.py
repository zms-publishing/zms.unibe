import os
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query
from sqlmodel import Session, select, inspect

from zms.unibe.fastapi.meta import Tags
from zms.unibe.maintenance.sqlmodels.ZMSSchedulerRegistry import ZMSSchedulerRegistry
from zms.unibe.utils.db import connect_sqldb
from zms.unibe.utils.zope.context import create_zope_app_context, get_zmsindex

router = APIRouter(prefix="/zms", tags=[Tags.scheduler])


@router.get(
    path="/scheduler/tasks",
    summary="Get tasks that will be processed by scheduler",
)
def get_scheduler_tasks(

):
    with Session(connect_sqldb()) as session:
        statement = select(ZMSSchedulerRegistry).where(
            ZMSSchedulerRegistry.processed_dt.is_(None))
        results = session.exec(statement)

        return results.all()


@router.post(
    path="/scheduler/tasks",
    summary="Update tasks that have been processed by scheduler",
)
def update_scheduler_tasks(
        uuids: list[UUID] = Query(None, description='Processed UUIDs'),
):
    if not isinstance(uuids, list):
        return []

    now = datetime.now()

    with Session(connect_sqldb()) as session:

        for uuid in uuids:
            statement = select(ZMSSchedulerRegistry).where(
                ZMSSchedulerRegistry.task_uuid == uuid).where(
                ZMSSchedulerRegistry.processed_dt.is_(None))
            results = session.exec(statement)

            for res in results.all():
                res.processed_dt = now
                session.add(res)
                session.commit()
                session.refresh(res)

        statement = select(ZMSSchedulerRegistry).where(
            ZMSSchedulerRegistry.processed_dt == now)
        results = session.exec(statement)

        return results.all()

@router.post(
    path="/scheduler/task/agenda/{upn}",
    summary="Schedule update of agenda(s) identified by User Principal Name (UPN)",
)
def schedule_agenda_update_by_upn(
        upn: str,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    
    zmsindex = context.zcatalog_index({
        "meta_id": "ZMSAgenda",
    })

    sqlengine = connect_sqldb()

    if not inspect(sqlengine).has_table(ZMSSchedulerRegistry.__name__.lower()):
        ZMSSchedulerRegistry.__table__.create(sqlengine)

    with Session(sqlengine) as session:
        for item in zmsindex:  # an UPN may by set for multiple ZMSAgenda objects
            obj = item.getObject()
            if obj.attr('include_outlook') and upn in obj.attr('outlook_upn'):
                session.add(ZMSSchedulerRegistry.from_agenda(obj))
                session.commit()

        statement = select(ZMSSchedulerRegistry).where(
            ZMSSchedulerRegistry.task_title == upn).where(
            ZMSSchedulerRegistry.exec_onchange == True).where(
            ZMSSchedulerRegistry.processed_dt.is_(None))
        results = session.exec(statement)

        return results.all()
