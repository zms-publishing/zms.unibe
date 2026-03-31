from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

from zms.unibe.utils.helpers import parse_uuid


class ZMSSurveyJSAttachments(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    attachment_uuid: UUID = Field(primary_key=True)
    attachment_name: str
    attachment_type: str
    attachment_data: str
    attachment_hash: str
    survey_uuid_zms: UUID
    survey_uuid_submit: UUID = Field(foreign_key="zmssurveyjssubmissions.survey_uuid_submit", ondelete="CASCADE")

    @classmethod
    def from_submit(cls, survey_obj, survey_uuid_submit, survey_blob):
        
        mapping = {
            'attachment_uuid': uuid4(),
            'attachment_name': survey_blob[0],  # see 
            'attachment_type': survey_blob[1],  # ZMSSurveyJSSubmissions.extract_blobs
            'attachment_data': survey_blob[2],  # for
            'attachment_hash': survey_blob[3],  # list of attachment tuples
            'survey_uuid_zms': parse_uuid(survey_obj.get_uid()),
            'survey_uuid_submit': survey_uuid_submit,
        }
        return cls.model_validate(mapping)
