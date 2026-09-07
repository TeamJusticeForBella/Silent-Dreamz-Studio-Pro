import json
from datetime import datetime
from enum import Enum
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


CoercedDict = Annotated[dict[str, Any], BeforeValidator(_coerce_json)]


class PacketType(str, Enum):
    state_bar = "state_bar"; appellate = "appellate"; demand = "demand"
    media = "media"; attorney_intake = "attorney_intake"; other = "other"


class PacketStatus(str, Enum):
    draft = "draft"; under_review = "under_review"; locked = "locked"; exported = "exported"


class PacketCreateRequest(BaseModel):
    packet_type: PacketType
    title: str
    target_name: str | None = None
    description_md: str | None = None
    settings: dict[str, Any] = {}


class PacketUpdateRequest(BaseModel):
    status: PacketStatus | None = None
    title: str | None = None
    target_name: str | None = None
    description_md: str | None = None
    settings: dict[str, Any] | None = None


class Packet(BaseModel):
    id: UUID
    packet_type: PacketType
    status: PacketStatus
    title: str
    target_name: str | None = None
    description_md: str | None = None
    settings: CoercedDict = {}
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class PacketListResponse(BaseModel):
    items: list[Packet]
    next_cursor: str | None = None


class AddExhibitRequest(BaseModel):
    evidence_id: UUID
    exhibit_label: str
    exhibit_title: str | None = None
    sort_order: int = 0
    notes_md: str | None = None


class ExportPacketRequest(BaseModel):
    watermark: str | None = None
    redaction: bool = False
    numbering: str = "alpha"
    include_hash_manifest: bool = True
