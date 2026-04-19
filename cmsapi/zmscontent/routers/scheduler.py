from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Query
from sqlmodel import Session, select

from zms.unibe.utils.db import connect_sqldb
from zms.unibe.maintenance.sqlmodels.ZMSSchedulerRegistry import ZMSSchedulerRegistry


router = APIRouter(
    prefix="/v3/zms",
    tags=["UniBE Web CMS (unibe.ch)"],
)


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
