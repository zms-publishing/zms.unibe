from fastapi import APIRouter
from sqlmodel import Session, select, inspect
from zms.unibe.utils.db import connect_sqldb

from zms.unibe.utils.zope.context import create_zope_app_context
from zms.unibe.maintenance.sqlmodels.ZMSSchedulerRegistry import ZMSSchedulerRegistry


router = APIRouter(
    prefix="/v3/zms",
    tags=["UniBE Web CMS (unibe.ch)"],
)


@router.post(
    path="/content/agenda/{upn}/schedule",
    summary="Schedule update of agenda(s) identified by User Principal Name (UPN)",
)
def schedule_agenda_update_by_upn(
        upn: str,
):
    context = create_zope_app_context()
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
