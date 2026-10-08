import json
from fastapi import APIRouter
from ..core.clients import opensearch_client, qdrant_client
from ..core.deps import WorkspaceId
from ..schemas.search import SearchResponse, SearchResult

router = APIRouter(prefix="/search", tags=["Search"])

OS_INDICES = ["bcc-evidence-v1", "bcc-incidents-v1", "bcc-drafts-v1", "bcc-packets-v1"]


async def _fulltext_search(wid: str, query: str, filters: dict | None) -> list[SearchResult]:
    must = [{"multi_match": {"query": query, "fields": [
        "title^3", "extracted_text", "ocr_text", "transcript_text",
        "summary_md", "narrative_md", "body_md", "description_md"]}}]
    filter_clauses = [{"term": {"workspace_id": wid}}]
    if filters:
        if "type" in filters: filter_clauses.append({"term": {"evidence_type": filters["type"]}})
        if "tags" in filters: filter_clauses.append({"terms": {"tags": filters["tags"]}})
    body = {"size": 50, "query": {"bool": {"must": must, "filter": filter_clauses}},
            "highlight": {"fields": {"extracted_text": {}, "ocr_text": {}, "body_md": {}, "title": {}}, "fragment_size": 200}}
    resp = await opensearch_client.search(index=",".join(OS_INDICES), body=body)
    results = []
    for hit in resp["hits"]["hits"]:
        src = hit["_source"]
        kind = "evidence"
        if "incident_id" in src: kind = "incident"
        elif "draft_type" in src: kind = "draft"
        elif "packet_type" in src: kind = "packet"
        snippet = None
        if "highlight" in hit:
            parts = []
            for v in hit["highlight"].values(): parts.extend(v)
            snippet = " ... ".join(parts[:3])
        doc_id = src.get("evidence_id") or src.get("incident_id") or src.get("draft_id") or src.get("packet_id", hit["_id"])
        results.append(SearchResult(kind=kind, id=doc_id, score=hit["_score"], snippet=snippet))
    return results


def _merge(ft: list[SearchResult], sem: list[SearchResult]) -> list[SearchResult]:
    k = 60; scores: dict[str, float] = {}; items: dict[str, SearchResult] = {}
    for rank, r in enumerate(ft):
        key = f"{r.kind}:{r.id}"; scores[key] = scores.get(key, 0) + 1/(k+rank+1); items[key] = r
    for rank, r in enumerate(sem):
        key = f"{r.kind}:{r.id}"; scores[key] = scores.get(key, 0) + 1/(k+rank+1)
        if key not in items: items[key] = r
    sorted_keys = sorted(scores, key=lambda x: scores[x], reverse=True)
    return [SearchResult(kind=items[k].kind, id=items[k].id, score=scores[k], snippet=items[k].snippet) for k in sorted_keys[:50]]


@router.get("", response_model=SearchResponse)
async def search(workspace_id: WorkspaceId, q: str, mode: str = "hybrid", filters: str | None = None):
    parsed = json.loads(filters) if filters else None
    wid = str(workspace_id)
    ft = await _fulltext_search(wid, q, parsed) if mode in ("fulltext", "hybrid") else []
    sem: list[SearchResult] = []  # Placeholder: semantic search requires embedding pipeline
    merged = _merge(ft, sem) if mode == "hybrid" else (sem if mode == "semantic" else ft)
    return SearchResponse(results=merged)
