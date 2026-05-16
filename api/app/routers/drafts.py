from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..core.deps import DBSession, WorkspaceId
from ..schemas.common import JobEnqueueResponse
from ..schemas.drafts import (Draft, DraftGenerateRequest, DraftListResponse,
                               DraftStatusUpdateRequest, DraftUpdateRequest)
from ..services.custody import log_custody_event
from ..services.nats_jobs import publish_job

router = APIRouter(prefix="/drafts", tags=["Drafts"])


@router.get("", response_model=DraftListResponse)
async def list_drafts(db: DBSession, workspace_id: WorkspaceId, status: str | None = None,
                      type: str | None = None, limit: int = 25, cursor: str | None = None):
    conds = ["workspace_id = :wid"]; params: dict = {"wid": str(workspace_id), "limit": limit}
    if status: conds.append("status = :status"); params["status"] = status
    if type: conds.append("draft_type = :type"); params["type"] = type
    if cursor: conds.append("created_at < :cursor"); params["cursor"] = cursor
    where = " AND ".join(conds)
    result = await db.execute(text(f"SELECT * FROM draft WHERE {where} ORDER BY created_at DESC LIMIT :limit"), params)
    rows = result.mappings().all()
    items = [Draft(**dict(r)) for r in rows]
    nc = str(items[-1].created_at.isoformat()) if len(items) == limit else None
    return DraftListResponse(items=items, next_cursor=nc)


@router.post("", response_model=JobEnqueueResponse, status_code=202)
async def generate_draft(workspace_id: WorkspaceId, body: DraftGenerateRequest):
    job_id = await publish_job(subject="bcc.jobs.draft.generate", kind="draft.generate",
        workspace_id=workspace_id, payload={
            "draft_type": body.draft_type.value, "title": body.title,
            "incident_id": str(body.incident_id) if body.incident_id else None,
            "packet_id": str(body.packet_id) if body.packet_id else None,
            "evidence_ids": [str(eid) for eid in body.evidence_ids],
            "agent": body.agent, "instructions": body.instructions})
    return JobEnqueueResponse(job_ids=[job_id])


@router.get("/{draft_id}", response_model=Draft)
async def get_draft(db: DBSession, workspace_id: WorkspaceId, draft_id: UUID):
    result = await db.execute(text("SELECT * FROM draft WHERE id = :id AND workspace_id = :wid"),
                              {"id": str(draft_id), "wid": str(workspace_id)})
    row = result.mappings().fetchone()
    if not row: raise HTTPException(status_code=404, detail="Draft not found")
    return Draft(**dict(row))


@router.patch("/{draft_id}", response_model=Draft)
async def update_draft(db: DBSession, workspace_id: WorkspaceId, draft_id: UUID, body: DraftUpdateRequest):
    updates = body.model_dump(exclude_unset=True)
    if not updates: raise HTTPException(status_code=400, detail="No fields to update")
    sets = []; params: dict = {"id": str(draft_id), "wid": str(workspace_id)}
    for k, v in updates.items(): sets.append(f"{k} = :{k}"); params[k] = v
    result = await db.execute(text(f"UPDATE draft SET {', '.join(sets)} WHERE id = :id AND workspace_id = :wid RETURNING *"), params)
    await db.commit()
    row = result.mappings().fetchone()
    if not row: raise HTTPException(status_code=404, detail="Draft not found")
    await log_custody_event(db, workspace_id=workspace_id, event_type="draft_edited",
                            subject_kind="draft", subject_id=draft_id, actor_agent="api")
    await db.commit()
    return Draft(**dict(row))


@router.post("/{draft_id}/status")
async def update_draft_status(db: DBSession, workspace_id: WorkspaceId, draft_id: UUID, body: DraftStatusUpdateRequest):
    result = await db.execute(text("UPDATE draft SET status = :status WHERE id = :id AND workspace_id = :wid RETURNING id"),
                              {"id": str(draft_id), "wid": str(workspace_id), "status": body.status.value})
    await db.commit()
    row = result.fetchone()
    if not row: raise HTTPException(status_code=404, detail="Draft not found")
    event_map = {"approved": "draft_approved", "rejected": "draft_rejected"}
    await log_custody_event(db, workspace_id=workspace_id,
                            event_type=event_map.get(body.status.value, "draft_edited"),
                            subject_kind="draft", subject_id=draft_id, actor_agent="api",
                            details={"new_status": body.status.value, "note": body.note})
    await db.commit()
    return {"status": body.status.value}
