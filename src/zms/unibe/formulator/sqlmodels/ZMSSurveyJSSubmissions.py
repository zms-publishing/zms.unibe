import json

from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field, Column, DateTime

from zms.unibe.utils.helpers import parse_uuid, local_timezone


class ZMSSurveyJSSubmissions(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    survey_uuid: UUID
    survey_path: str
    survey_data_json: str
    survey_submitted_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    @classmethod
    def from_submit(cls, survey):
        try:
            # sanitize submitted data
            data_json = json.loads(survey.REQUEST.form.get('data'))
        except Exception as e:
            raise ValueError(f"Invalid JSON data in survey submission: {e}")

        mapping = {
            'id': None,
            'survey_uuid': parse_uuid(survey.get_uid()),
            'survey_path': survey.getPath(),
            'survey_data_json': json.dumps(data_json, indent=4, sort_keys=True, default=str),
            'survey_submitted_at': local_timezone(datetime.now()),
        }
        return cls.model_validate(mapping), data_json
