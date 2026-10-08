from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID
from pydantic import BaseModel


class DraftType(str, Enum):
    declaration = "declaration"; demand_letter = "demand_letter"; bar_complaint = "bar_complaint"
    appellate_packet = "appellate_packet"; email = "email"; exhibit_list = "exhibit_list"
    memo = "memo"; other = "other"


class DraftStatus(str, Enum):
    needs_review = "needs_review"; approved = "approved"; rejected = "rejected"
    needs_evidence = "needs_evidence"; in_progress = "in_progress"


class DraftGenerateRequest(BaseModel):
    draft_type: DraftType
    title: str
    incident_id: UUID | None = None
    packet_id: UUID | None = None
    evidence_ids: list[UUID] = []
    agent: str | None = None
    instructions: str | None = None


class DraftUpdateRequest(BaseModel):
    title: str | None = None
    body_md: str | None = None
    metadata: dict[str, Any] | None = None


class DraftStatusUpdateRequest(BaseModel):
    status: DraftStatus
    note: str | None = None


class Draft(BaseModel):
    id: UUID
    draft_type: DraftType
    status: DraftStatus
    title: str
    body_md: str
    body_rendered: str | None = None
    metadata: dict[str, Any]
    incident_id: UUID | None = None
    packet_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class DraftListResponse(BaseModel):
    items: list[Draft]
    next_cursor: str | None = None
