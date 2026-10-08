from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel


class CitationCreateRequest(BaseModel):
    evidence_id: UUID | None = None
    citation_kind: str
    page_number: int | None = None
    bbox: dict[str, Any] | None = None
    text_quote: str | None = None
    transcript_start_ms: int | None = None
    transcript_end_ms: int | None = None
    url: str | None = None


class CitationAnchor(BaseModel):
    id: UUID
    evidence_id: UUID | None = None
    citation_kind: str
    page_number: int | None = None
    bbox: dict[str, Any] | None = None
    text_quote: str | None = None
    transcript_start_ms: int | None = None
    transcript_end_ms: int | None = None
    url: str | None = None
    sha256_context: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True


class DraftCitationAttachRequest(BaseModel):
    anchor_id: UUID
    selector: str
    note: str | None = None
