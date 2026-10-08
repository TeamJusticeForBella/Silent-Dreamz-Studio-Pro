from uuid import UUID
from fastapi import APIRouter
from sqlalchemy import text
from ..core.deps import DBSession, WorkspaceId
from ..schemas.common import ExportArtifact, ExportListResponse

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get("", response_model=ExportListResponse)
async def list_exports(db: DBSession, workspace_id: WorkspaceId,
                       packetId: UUID | None = None, draftId: UUID | None = None):
    conds = ["workspace_id = :wid"]; params: dict = {"wid": str(workspace_id)}
    if packetId: conds.append("packet_id = :pid"); params["pid"] = str(packetId)
    if draftId: conds.append("draft_id = :did"); params["did"] = str(draftId)
    where = " AND ".join(conds)
    result = await db.execute(text(f"SELECT * FROM export_artifact WHERE {where} ORDER BY created_at DESC"), params)
    rows = result.mappings().all()
    return ExportListResponse(items=[ExportArtifact(**dict(r)) for r in rows])
