from typing import Annotated, Generator

from fastapi import Depends, Request
from redis import Redis
from rq import Queue
from sqlmodel import Session

from OFS.Application import Application
from ..utils.zope.context import create_zope_app_context


def get_sqldb_session(request: Request) -> Generator[Session, None, None]:
    with Session(request.app.main_state.sqldb_engine) as session:
        yield session  # Connection remains open for the request
                       # closes automatically after

SessionDependency = Annotated[Session, Depends(get_sqldb_session)]


def get_zope_context() -> Application:
    return create_zope_app_context()

ContextDependency = Annotated[Application, Depends(get_zope_context)]


def get_redis_connection(request: Request) -> Generator[Redis, None, None]:
    with request.app.main_state.redis_connection as client:
        yield client

CacheDependency = Annotated[Redis, Depends(get_redis_connection)]


def get_redis_queue(request: Request) -> Queue:
    return request.app.main_state.redis_queue

QueueDependency = Annotated[Queue, Depends(get_redis_queue)]
