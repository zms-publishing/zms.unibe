from datetime import datetime, timezone
from typing import Annotated

from pydantic import AwareDatetime
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, String

PostgreSQLArray = Annotated[
    list,
    Field(
        default=None,
        sa_type=postgresql.ARRAY(String()),
    )
]

OptionalDateTime = Annotated[
    AwareDatetime | None,
    Field(
        nullable=True,
        sa_type=postgresql.TIMESTAMP(timezone=True),
        default_factory=None,
    )
]

OptionalDateTimeOnUpdate = Annotated[
    AwareDatetime | None,
    Field(
        nullable=True,
        sa_type=postgresql.TIMESTAMP(timezone=True),
        default_factory=None,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )
]

RequiredDateTimeNow = Annotated[
    AwareDatetime,
    Field(
        nullable=False,
        sa_type=postgresql.TIMESTAMP(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc)
    )
]

RequiredDateTimeOnUpdate = Annotated[
    AwareDatetime,
    Field(
        nullable=False,
        sa_type=postgresql.TIMESTAMP(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )
]