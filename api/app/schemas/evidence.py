from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class EvidenceType(str, Enum):
    pdf = "pdf"; doc = "doc"; docx = "docx"; txt = "txt"; email = "email"
    image = "image"; audio = "audio"; video = "video"; zip = "zip"; other = "other"


class EvidenceCreateRequest(BaseModel):
    title: str
    evidence_type: EvidenceType
    sha256: str
    source_kind: str | None = None
    source_ref: str | None = None
    content_mime: str | None = None
    size_bytes: int | None = None
    event_time_start: datetime | None = None
    event_time_end: datetime | None = None
    tags: list[str] = []
    metadata: dict[str, Any] = {}


class EvidenceUpdateRequest(BaseModel):
    title: str | None = None
    is_key_evidence: bool | None = None
    tags: list[str] | None = None
    event_time_start: datetime | None = None
    event_time_end: datetime | None = None
    metadata: dict[str, Any] | None = None


class EvidenceItem(BaseModel):
    id: UUID
    title: str
    evidence_type: EvidenceType
    source_kind: str | None = None
    source_ref: str | None = None
    object_bucket: str
    object_key: str
    object_etag: str | None = None
    size_bytes: int | None = None
    sha256: str
    content_mime: str | None = None
    event_time_start: datetime | None = None
    event_time_end: datetime | None = None
    uploaded_at: datetime
    extracted_text_key: str | None = None
    ocr_text_key: str | None = None
    transcript_key: str | None = None
    preview_key: str | None = None
    is_key_evidence: bool
    tags: list[str]
    metadata: dict[str, Any]
    class Config:
        from_attributes = True


class EvidenceListResponse(BaseModel):
    items: list[EvidenceItem]
    next_cursor: str | None = None


class PresignRequest(BaseModel):
    filename: str
    content_mime: str | None = None


class PresignResponse(BaseModel):
    upload_url: str
    object_bucket: str
    object_key: str
    headers: dict[str, str] = {}


class EvidenceFinalizeRequest(BaseModel):
    object_bucket: str
    object_key: str
    object_etag: str | None = None
    size_bytes: int | None = None
    verify_sha256: bool = True
