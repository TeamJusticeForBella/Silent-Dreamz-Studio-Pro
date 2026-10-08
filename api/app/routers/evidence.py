from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..core.deps import DBSession, WorkspaceId
from ..schemas.common import JobEnqueueResponse
from ..schemas.evidence import (
    EvidenceCreateRequest, EvidenceFinalizeRequest, EvidenceItem,
    EvidenceListResponse, EvidenceUpdateRequest, PresignRequest, PresignResponse,
)
from ..services.custody import log_custody_event
from ..services.nats_jobs import publish_job

router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.get("", response_model=EvidenceListResponse)
async def list_evidence(db: DBSession, workspace_id: WorkspaceId, q: str | None = None,
                        type: str | None = None, tag: str | None = None,
                        key: bool | None = None, limit: int = 25, cursor: str | None = None):
    conds = ["workspace_id = :wid"]
    params: dict = {"wid": str(workspace_id), "limit": limit}
    if q:
        conds.append("title ILIKE :q"); params["q"] = f"%{q}%"
    if type:
        conds.append("evidence_type = :type"); params["type"] = type
    if tag:
        conds.append(":tag = ANY(tags)"); params["tag"] = tag
    if key is not None:
        conds.append("is_key_evidence = :key"); params["key"] = key
    if cursor:
        conds.append("uploaded_at < :cursor"); params["cursor"] = cursor
    where = " AND ".join(conds)
    result = await db.execute(text(f"SELECT * FROM evidence_item WHERE {where} ORDER BY uploaded_at DESC LIMIT :limit"), params)
    rows = result.mappings().all()
    items = [EvidenceItem(**dict(r)) for r in rows]
    nc = str(items[-1].uploaded_at.isoformat()) if len(items) == limit else None
    return EvidenceListResponse(items=items, next_cursor=nc)


@router.post("", response_model=EvidenceItem, status_code=201)
async def create_evidence(db: DBSession, workspace_id: WorkspaceId, body: EvidenceCreateRequest):
    eid = uuid4()
    okey = f"{workspace_id}/{eid}/{body.title}"
    result = await db.execute(text("""
        INSERT INTO evidence_item (id, workspace_id, title, evidence_type, sha256, object_key,
            source_kind, source_ref, content_mime, size_bytes, event_time_start, event_time_end, tags, metadata)
        VALUES (:id, :wid, :title, :etype, :sha256, :okey, :sk, :sr, :cm, :sb, :ets, :ete, :tags, :meta)
        RETURNING *"""),
        {"id": str(eid), "wid": str(workspace_id), "title": body.title, "etype": body.evidence_type.value,
         "sha256": body.sha256, "okey": okey, "sk": body.source_kind, "sr": body.source_ref,
         "cm": body.content_mime, "sb": body.size_bytes, "ets": body.event_time_start,
         "ete": body.event_time_end, "tags": body.tags, "meta": body.metadata})
    await db.commit()
    row = result.mappings().fetchone()
    await log_custody_event(db, workspace_id=workspace_id, event_type="ingested",
                            subject_kind="evidence_item", subject_id=eid, actor_agent="api",
                            details={"sha256": body.sha256})
    await db.commit()
    return EvidenceItem(**dict(row))


@router.get("/{evidence_id}", response_model=EvidenceItem)
async def get_evidence(db: DBSession, workspace_id: WorkspaceId, evidence_id: UUID):
    result = await db.execute(text("SELECT * FROM evidence_item WHERE id = :id AND workspace_id = :wid"),
                              {"id": str(evidence_id), "wid": str(workspace_id)})
    row = result.mappings().fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return EvidenceItem(**dict(row))


@router.patch("/{evidence_id}", response_model=EvidenceItem)
async def update_evidence(db: DBSession, workspace_id: WorkspaceId, evidence_id: UUID, body: EvidenceUpdateRequest):
    updates = body.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    sets = []; params: dict = {"id": str(evidence_id), "wid": str(workspace_id)}
    for k, v in updates.items():
        sets.append(f"{k} = :{k}"); params[k] = v
    result = await db.execute(text(f"UPDATE evidence_item SET {', '.join(sets)} WHERE id = :id AND workspace_id = :wid RETURNING *"), params)
    await db.commit()
    row = result.mappings().fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return EvidenceItem(**dict(row))


@router.post("/{evidence_id}/upload-url", response_model=PresignResponse)
async def get_upload_url(workspace_id: WorkspaceId, evidence_id: UUID, body: PresignRequest):
    from ..core.clients import s3_client
    from ..core.config import settings
    okey = f"{workspace_id}/{evidence_id}/{body.filename}"
    url = s3_client.generate_presigned_url("put_object",
        Params={"Bucket": settings.MINIO_BUCKET_EVIDENCE, "Key": okey,
                "ContentType": body.content_mime or "application/octet-stream"}, ExpiresIn=3600)
    return PresignResponse(upload_url=url, object_bucket=settings.MINIO_BUCKET_EVIDENCE, object_key=okey)


@router.post("/{evidence_id}/finalize", response_model=JobEnqueueResponse, status_code=202)
async def finalize_evidence(db: DBSession, workspace_id: WorkspaceId, evidence_id: UUID, body: EvidenceFinalizeRequest):
    await db.execute(text("""UPDATE evidence_item SET object_key = :okey, object_bucket = :ob,
        object_etag = :oe, size_bytes = :sb WHERE id = :id AND workspace_id = :wid"""),
        {"id": str(evidence_id), "wid": str(workspace_id), "okey": body.object_key,
         "ob": body.object_bucket, "oe": body.object_etag, "sb": body.size_bytes})
    await db.commit()
    job_id = await publish_job(subject="bcc.jobs.ingest.finalize", kind="ingest.finalize",
        workspace_id=workspace_id, payload={"evidence_id": str(evidence_id),
            "object_bucket": body.object_bucket, "object_key": body.object_key,
            "verify_sha256": body.verify_sha256})
    return JobEnqueueResponse(job_ids=[job_id])
