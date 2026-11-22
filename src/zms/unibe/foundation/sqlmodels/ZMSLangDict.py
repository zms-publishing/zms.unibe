from sqlmodel import Field, SQLModel


class ZMSLangDict(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    key: str = Field(primary_key=True)
    ger: str | None = None
    eng: str | None = None
    fra: str | None = None
    ita: str | None = None
    spa: str | None = None
    esp: str | None = None
    ned: str | None = None
    chi: str | None = None
    fas: str | None = None
    rus: str | None = None
    hin: str | None = None
    ara: str | None = None
    vie: str | None = None
    heb: str | None = None


    @staticmethod
    def get_zms_catalog_query():
        return 'langdict'
    