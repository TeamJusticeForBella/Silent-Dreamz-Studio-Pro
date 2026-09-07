from uuid import UUID
from pydantic import BaseModel


class SearchAnchor(BaseModel):
    page_number: int | None = None
    transcript_ms: int | None = None


class SearchResult(BaseModel):
    kind: str
    id: UUID
    score: float
    snippet: str | None = None
    anchors: list[SearchAnchor] = []


class SearchResponse(BaseModel):
    results: list[SearchResult]
