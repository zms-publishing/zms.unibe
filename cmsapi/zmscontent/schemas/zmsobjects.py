from uuid import UUID

from pydantic import BaseModel


class ZMSSite(BaseModel):  # Response schema
    sitePath: str
    siteType: str | None
    siteTitle: str
    siteShort: str
    siteAlias: str | None
    siteDomain: str | None
    siteUuid: UUID
    siteParentUuid: UUID


class ZMSDocument(BaseModel):  # TODO: apply Response schema to router
    documentTitle: str
    documentSite: str
    documentUuid: UUID


class ZMSFolder(BaseModel):  # TODO: apply Response schema to router
    folderTitle: str
    folderSite: str
    folderUuid: UUID


class ZMSFormulator(BaseModel):  # TODO: apply Response schema to router
    formTitle: str
    formSite: str
    formUuid: UUID


class ZMSDataTable(BaseModel):  # TODO: apply Response schema to router
    datatablePath: str
    datatableUrl: str | None
    datatableSite: str
    datatableDomain: str
