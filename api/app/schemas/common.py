from uuid import UUID
from pydantic import BaseModel


class JobEnqueueResponse(BaseModel):
    job_ids: list[UUID]


class ExportArtifact(BaseModel):
    id: UUID
    kind: str
    title: str
    packet_id: UUID | None = None
    draft_id: UUID | None = None
    object_bucket: str
    object_key: str
    sha256: str
    size_bytes: int | None = None
    class Config:
        from_attributes = True


class ExportListResponse(BaseModel):
    items: list[ExportArtifact]
