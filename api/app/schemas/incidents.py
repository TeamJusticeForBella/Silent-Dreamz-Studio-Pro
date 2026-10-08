import json
from datetime import datetime
from typing import Annotated, Any
from uuid import UUID
from pydantic import BaseModel, BeforeValidator


def _coerce_json(v: Any) -> Any:
    if isinstance(v, str):
        try:
            return json.loads(v)
        except (json.JSONDecodeError, TypeError):
            pass
    return v


CoercedList = Annotated[list[str], BeforeValidator(_coerce_json)]


class IncidentCreateRequest(BaseModel):
    title: str
    summary_md: str | None = None
    narrative_md: str | None = None
    allegation_tags: list[str] = []
    incident_time_start: datetime | None = None
    incident_time_end: datetime | None = None


class IncidentUpdateRequest(BaseModel):
    title: str | None = None
    status: str | None = None
    summary_md: str | None = None
    narrative_md: str | None = None
    allegation_tags: list[str] | None = None
    incident_time_start: datetime | None = None
    incident_time_end: datetime | None = None


class Incident(BaseModel):
    id: UUID
    title: str
    status: str
    summary_md: str | None = None
    narrative_md: str | None = None
    allegation_tags: CoercedList = []
    incident_time_start: datetime | None = None
    incident_time_end: datetime | None = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class IncidentListResponse(BaseModel):
    items: list[Incident]
    next_cursor: str | None = None


class IncidentLinkEvidenceRequest(BaseModel):
    evidence_id: UUID
    sort_order: int = 0
    note: str | None = None
