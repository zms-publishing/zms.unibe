from fastapi import Depends, Request
from sqlmodel import Session
from typing import Annotated, Generator
from OFS.Application import Application
from redis import Redis
from rq import Queue

from zms.unibe.utils.zope.context import create_zope_app_context


def get_session(request: Request) -> Generator[Session, None, None]:
    with Session(request.app.main_state.sqldb_engine) as session:
        yield session  # Connection remains open for the request
                       # closes automatically after

SessionDependency = Annotated[Session, Depends(get_session)]


def get_context() -> Application:
    return create_zope_app_context()

ContextDependency = Annotated[Application, Depends(get_context)]


def get_cache(request: Request) -> Generator[Redis, None, None]:
    with request.app.main_state.redis_cache_conn as client:
        yield client

CacheDependency = Annotated[Redis, Depends(get_cache)]


def get_queue_conn(request: Request) -> Redis:
    return request.app.main_state.redis_queue_conn

QueueConnDependency = Annotated[Redis, Depends(get_queue_conn)]


def get_queue_jobs(request: Request) -> Queue:
    return request.app.main_state.redis_queue_jobs

QueueJobsDependency = Annotated[Queue, Depends(get_queue_jobs)]
