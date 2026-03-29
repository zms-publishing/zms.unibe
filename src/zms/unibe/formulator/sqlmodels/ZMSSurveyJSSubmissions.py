import json
import hashlib
import re

from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field, Column, DateTime

from zms.unibe.utils.helpers import parse_uuid, local_timezone


class ZMSSurveyJSSubmissions(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    survey_uuid_submit: UUID = Field(primary_key=True)
    survey_uuid_zms: UUID
    survey_path_zms: str
    survey_data_json: str
    survey_submitted_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    @classmethod
    def from_submit(cls, survey_obj, survey_uuid_submit):
        try:
            # sanitize submitted data
            data_json = json.loads(survey_obj.REQUEST.form.get('data'))
        except Exception as e:
            raise ValueError(f"Invalid JSON data in survey submission: {e}")

        data_json, data_blobs = cls.extract_blobs(json.dumps(data_json, indent=4, sort_keys=True, default=str))
            
        mapping = {
            'survey_uuid_submit': survey_uuid_submit,
            'survey_uuid_zms': parse_uuid(survey_obj.get_uid()),
            'survey_path_zms': survey_obj.getPath(),
            'survey_data_json': json.dumps(data_json, indent=4, sort_keys=True, default=str),
            'survey_submitted_at': local_timezone(datetime.now()),
        }
        return cls.model_validate(mapping), data_json, data_blobs

    @staticmethod
    def extract_blobs(json_string_original):
        pattern = r'"data:([^;]+);base64,([A-Za-z0-9+/=]+)"'

        data_blobs = []
        matches = re.findall(pattern, json_string_original)
        json_string_trimmed = json_string_original
        for match in matches:
            mime_type, data_content = match
            file_name = f'attachment.{mime_type.split('/')[1]}'  # TODO: extract file_name as well
            data_hash = hashlib.sha256(data_content.encode()).hexdigest()
            data_blobs.append((file_name, mime_type, data_content, data_hash))  # list of attachment tuples
            json_string_trimmed = json_string_trimmed.replace(f';base64,{data_content}', f';sha256,{data_hash}')
        try:
            data_json = json.loads(json_string_trimmed)
        except Exception as e:
            raise ValueError(f"Invalid JSON data in survey submission: {e}")
        
        return data_json, data_blobs
