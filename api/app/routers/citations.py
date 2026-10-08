from uuid import UUID, uuid4
from fastapi import APIRouter
from sqlalchemy import text
from ..core.deps import DBSession, WorkspaceId
from ..schemas.citations import CitationAnchor, CitationCreateRequest, DraftCitationAttachRequest

router = APIRouter(tags=["Citations"])


@router.post("/citations", response_model=CitationAnchor, status_code=201)
async def create_citation(db: DBSession, workspace_id: WorkspaceId, body: CitationCreateRequest):
    cid = uuid4()
    result = await db.execute(text("""
        INSERT INTO citation_anchor (id, workspace_id, evidence_id, citation_kind,
            page_number, bbox, text_quote, transcript_start_ms, transcript_end_ms, url)
        VALUES (:id, :wid, :eid, :kind, :page, :bbox, :quote, :ts_start, :ts_end, :url) RETURNING *"""),
        {"id": str(cid), "wid": str(workspace_id),
         "eid": str(body.evidence_id) if body.evidence_id else None,
         "kind": body.citation_kind, "page": body.page_number, "bbox": body.bbox,
         "quote": body.text_quote, "ts_start": body.transcript_start_ms,
         "ts_end": body.transcript_end_ms, "url": body.url})
    await db.commit()
    return CitationAnchor(**dict(result.mappings().fetchone()))


@router.post("/drafts/{draft_id}/citations")
async def attach_citation(db: DBSession, workspace_id: WorkspaceId, draft_id: UUID, body: DraftCitationAttachRequest):
    await db.execute(text("""INSERT INTO draft_citation (draft_id, anchor_id, selector, note)
        VALUES (:did, :aid, :sel, :note)
        ON CONFLICT (draft_id, anchor_id, selector) DO UPDATE SET note = :note"""),
        {"did": str(draft_id), "aid": str(body.anchor_id), "sel": body.selector, "note": body.note})
    await db.commit()
    return {"status": "attached"}
