from fastapi import Depends
from sqlmodel import Session
from typing import Annotated, Generator
from OFS.Application import Application

from zms.unibe.utils.zope.context import create_zope_app_context


def get_session() -> Generator[Session, None, None]:
    from app.main import SQLDB_ENGINE
    with Session(SQLDB_ENGINE) as session:
        yield session  # Connection remains open for the request
                       # closes automatically after

SessionDependency = Annotated[Session, Depends(get_session)]


def get_context():
    return create_zope_app_context()

ContextDependency = Annotated[Application, Depends(get_context)]
