from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..core.deps import DBSession, WorkspaceId
from ..schemas.common import JobEnqueueResponse
from ..schemas.packets import (AddExhibitRequest, ExportPacketRequest, Packet, PacketCreateRequest,
                                PacketListResponse, PacketUpdateRequest)
from ..services.custody import log_custody_event
from ..services.nats_jobs import publish_job

router = APIRouter(prefix="/packets", tags=["Packets"])


@router.get("", response_model=PacketListResponse)
async def list_packets(db: DBSession, workspace_id: WorkspaceId, type: str | None = None,
                       status: str | None = None, limit: int = 25, cursor: str | None = None):
    conds = ["workspace_id = :wid"]; params: dict = {"wid": str(workspace_id), "limit": limit}
    if type: conds.append("packet_type = :type"); params["type"] = type
    if status: conds.append("status = :status"); params["status"] = status
    if cursor: conds.append("created_at < :cursor"); params["cursor"] = cursor
    where = " AND ".join(conds)
    result = await db.execute(text(f"SELECT * FROM packet WHERE {where} ORDER BY created_at DESC LIMIT :limit"), params)
    rows = result.mappings().all()
    items = [Packet(**dict(r)) for r in rows]
    nc = str(items[-1].created_at.isoformat()) if len(items) == limit else None
    return PacketListResponse(items=items, next_cursor=nc)


@router.post("", response_model=Packet, status_code=201)
async def create_packet(db: DBSession, workspace_id: WorkspaceId, body: PacketCreateRequest):
    pid = uuid4()
    result = await db.execute(text("""
        INSERT INTO packet (id, workspace_id, packet_type, title, target_name, description_md, settings)
        VALUES (:id, :wid, :pt, :title, :target, :desc, :settings) RETURNING *"""),
        {"id": str(pid), "wid": str(workspace_id), "pt": body.packet_type.value,
         "title": body.title, "target": body.target_name, "desc": body.description_md, "settings": body.settings})
    await db.commit()
    return Packet(**dict(result.mappings().fetchone()))


@router.get("/{packet_id}", response_model=Packet)
async def get_packet(db: DBSession, workspace_id: WorkspaceId, packet_id: UUID):
    result = await db.execute(text("SELECT * FROM packet WHERE id = :id AND workspace_id = :wid"),
                              {"id": str(packet_id), "wid": str(workspace_id)})
    row = result.mappings().fetchone()
    if not row: raise HTTPException(status_code=404, detail="Packet not found")
    return Packet(**dict(row))


@router.patch("/{packet_id}", response_model=Packet)
async def update_packet(db: DBSession, workspace_id: WorkspaceId, packet_id: UUID, body: PacketUpdateRequest):
    updates = body.model_dump(exclude_unset=True)
    if not updates: raise HTTPException(status_code=400, detail="No fields to update")
    sets = []; params: dict = {"id": str(packet_id), "wid": str(workspace_id)}
    for k, v in updates.items():
        if k == "status" and v is not None: v = v.value
        sets.append(f"{k} = :{k}"); params[k] = v
    result = await db.execute(text(f"UPDATE packet SET {', '.join(sets)} WHERE id = :id AND workspace_id = :wid RETURNING *"), params)
    await db.commit()
    row = result.mappings().fetchone()
    if not row: raise HTTPException(status_code=404, detail="Packet not found")
    return Packet(**dict(row))


@router.post("/{packet_id}/exhibits")
async def add_exhibit(db: DBSession, workspace_id: WorkspaceId, packet_id: UUID, body: AddExhibitRequest):
    await db.execute(text("""INSERT INTO packet_exhibit (packet_id, evidence_id, exhibit_label, exhibit_title, sort_order, notes_md)
        VALUES (:pid, :eid, :label, :title, :sort, :notes)
        ON CONFLICT (packet_id, evidence_id) DO UPDATE SET exhibit_label = :label, exhibit_title = :title, sort_order = :sort, notes_md = :notes"""),
        {"pid": str(packet_id), "eid": str(body.evidence_id), "label": body.exhibit_label,
         "title": body.exhibit_title, "sort": body.sort_order, "notes": body.notes_md})
    await db.commit()
    await log_custody_event(db, workspace_id=workspace_id, event_type="added_to_packet",
                            subject_kind="evidence_item", subject_id=body.evidence_id, actor_agent="api",
                            details={"packet_id": str(packet_id), "exhibit_label": body.exhibit_label})
    await db.commit()
    return {"status": "added"}


@router.delete("/{packet_id}/exhibits")
async def remove_exhibit(db: DBSession, workspace_id: WorkspaceId, packet_id: UUID, evidenceId: UUID):
    await db.execute(text("DELETE FROM packet_exhibit WHERE packet_id = :pid AND evidence_id = :eid"),
                     {"pid": str(packet_id), "eid": str(evidenceId)})
    await db.commit()
    await log_custody_event(db, workspace_id=workspace_id, event_type="removed_from_packet",
                            subject_kind="evidence_item", subject_id=evidenceId, actor_agent="api",
                            details={"packet_id": str(packet_id)})
    await db.commit()
    return {"status": "removed"}


@router.post("/{packet_id}/export", response_model=JobEnqueueResponse, status_code=202)
async def export_packet(workspace_id: WorkspaceId, packet_id: UUID, body: ExportPacketRequest):
    job_id = await publish_job(subject="bcc.jobs.export.packet", kind="export.packet",
        workspace_id=workspace_id, payload={"packet_id": str(packet_id), "watermark": body.watermark,
            "redaction": body.redaction, "numbering": body.numbering,
            "include_hash_manifest": body.include_hash_manifest})
    return JobEnqueueResponse(job_ids=[job_id])
