from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..core.deps import DBSession, WorkspaceId
from ..schemas.incidents import (Incident, IncidentCreateRequest, IncidentLinkEvidenceRequest,
                                  IncidentListResponse, IncidentUpdateRequest)
from ..services.custody import log_custody_event

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("", response_model=IncidentListResponse)
async def list_incidents(db: DBSession, workspace_id: WorkspaceId, q: str | None = None,
                         limit: int = 25, cursor: str | None = None):
    conds = ["workspace_id = :wid"]; params: dict = {"wid": str(workspace_id), "limit": limit}
    if q: conds.append("title ILIKE :q"); params["q"] = f"%{q}%"
    if cursor: conds.append("created_at < :cursor"); params["cursor"] = cursor
    where = " AND ".join(conds)
    result = await db.execute(text(f"SELECT * FROM incident WHERE {where} ORDER BY created_at DESC LIMIT :limit"), params)
    rows = result.mappings().all()
    items = [Incident(**dict(r)) for r in rows]
    nc = str(items[-1].created_at.isoformat()) if len(items) == limit else None
    return IncidentListResponse(items=items, next_cursor=nc)


@router.post("", response_model=Incident, status_code=201)
async def create_incident(db: DBSession, workspace_id: WorkspaceId, body: IncidentCreateRequest):
    iid = uuid4()
    result = await db.execute(text("""
        INSERT INTO incident (id, workspace_id, title, summary_md, narrative_md, allegation_tags, incident_time_start, incident_time_end)
        VALUES (:id, :wid, :title, :summary, :narrative, :tags, :ts, :te) RETURNING *"""),
        {"id": str(iid), "wid": str(workspace_id), "title": body.title, "summary": body.summary_md,
         "narrative": body.narrative_md, "tags": body.allegation_tags,
         "ts": body.incident_time_start, "te": body.incident_time_end})
    await db.commit()
    return Incident(**dict(result.mappings().fetchone()))


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(db: DBSession, workspace_id: WorkspaceId, incident_id: UUID):
    result = await db.execute(text("SELECT * FROM incident WHERE id = :id AND workspace_id = :wid"),
                              {"id": str(incident_id), "wid": str(workspace_id)})
    row = result.mappings().fetchone()
    if not row: raise HTTPException(status_code=404, detail="Incident not found")
    return Incident(**dict(row))


@router.patch("/{incident_id}", response_model=Incident)
async def update_incident(db: DBSession, workspace_id: WorkspaceId, incident_id: UUID, body: IncidentUpdateRequest):
    updates = body.model_dump(exclude_unset=True)
    if not updates: raise HTTPException(status_code=400, detail="No fields to update")
    sets = []; params: dict = {"id": str(incident_id), "wid": str(workspace_id)}
    for k, v in updates.items(): sets.append(f"{k} = :{k}"); params[k] = v
    result = await db.execute(text(f"UPDATE incident SET {', '.join(sets)} WHERE id = :id AND workspace_id = :wid RETURNING *"), params)
    await db.commit()
    row = result.mappings().fetchone()
    if not row: raise HTTPException(status_code=404, detail="Incident not found")
    return Incident(**dict(row))


@router.post("/{incident_id}/evidence")
async def link_evidence(db: DBSession, workspace_id: WorkspaceId, incident_id: UUID, body: IncidentLinkEvidenceRequest):
    await db.execute(text("""INSERT INTO incident_evidence (incident_id, evidence_id, sort_order, note)
        VALUES (:iid, :eid, :sort, :note)
        ON CONFLICT (incident_id, evidence_id) DO UPDATE SET sort_order = :sort, note = :note"""),
        {"iid": str(incident_id), "eid": str(body.evidence_id), "sort": body.sort_order, "note": body.note})
    await db.commit()
    await log_custody_event(db, workspace_id=workspace_id, event_type="linked_incident",
                            subject_kind="evidence_item", subject_id=body.evidence_id, actor_agent="api",
                            details={"incident_id": str(incident_id)})
    await db.commit()
    return {"status": "linked"}


@router.delete("/{incident_id}/evidence")
async def unlink_evidence(db: DBSession, workspace_id: WorkspaceId, incident_id: UUID, evidenceId: UUID):
    await db.execute(text("DELETE FROM incident_evidence WHERE incident_id = :iid AND evidence_id = :eid"),
                     {"iid": str(incident_id), "eid": str(evidenceId)})
    await db.commit()
    await log_custody_event(db, workspace_id=workspace_id, event_type="unlinked_incident",
                            subject_kind="evidence_item", subject_id=evidenceId, actor_agent="api",
                            details={"incident_id": str(incident_id)})
    await db.commit()
    return {"status": "unlinked"}
