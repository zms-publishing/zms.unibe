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

OptionalUTCNow = Annotated[
    AwareDatetime | None,
    Field(
        nullable=True,
        default_factory=lambda: datetime.now(timezone.utc),
    )
]

OptionalUTCUpdate = Annotated[
    AwareDatetime | None,
    Field(
        nullable=True,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )
]

RequiredUTCNow = Annotated[
    AwareDatetime,
    Field(
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc)
    )
]

RequiredUTCUpdate = Annotated[
    AwareDatetime,
    Field(
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )
]