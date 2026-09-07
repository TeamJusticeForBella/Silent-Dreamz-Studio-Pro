"""Shared fixtures for BCC API tests.

Uses an in-memory SQLite database so tests run without Postgres, MinIO,
NATS, OpenSearch, or Qdrant.  External-service dependencies are stubbed.
"""
import asyncio
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.app.core.auth import create_access_token
from api.app.core.database import get_db

WS_A_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
WS_B_ID = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
USER_A_ID = uuid4()
USER_B_ID = uuid4()
USER_INACTIVE_ID = uuid4()

engine = create_async_engine("sqlite+aiosqlite://", echo=False)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


import json as _json
import sqlite3


def _adapt_list(val):
    return _json.dumps(val)


def _adapt_dict(val):
    return _json.dumps(val)


sqlite3.register_adapter(list, _adapt_list)
sqlite3.register_adapter(dict, _adapt_dict)


class _JsonStr(str):
    """A str subclass that Pydantic can parse as list or dict via validator."""
    pass


@event.listens_for(engine.sync_engine, "connect")
def _enable_fk(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA foreign_keys = ON")


DDL = """
CREATE TABLE IF NOT EXISTS workspace (
    id   TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS app_user (
    id            TEXT PRIMARY KEY,
    workspace_id  TEXT NOT NULL REFERENCES workspace(id),
    email         TEXT NOT NULL,
    display_name  TEXT,
    role          TEXT NOT NULL DEFAULT 'member',
    is_active     BOOLEAN NOT NULL DEFAULT 1,
    UNIQUE (workspace_id, email)
);

CREATE TABLE IF NOT EXISTS evidence_item (
    id              TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL REFERENCES workspace(id),
    title           TEXT NOT NULL,
    evidence_type   TEXT NOT NULL DEFAULT 'other',
    sha256          TEXT NOT NULL,
    object_key      TEXT NOT NULL,
    source_kind     TEXT,
    source_ref      TEXT,
    content_mime    TEXT,
    size_bytes      INTEGER,
    object_bucket   TEXT DEFAULT 'evidence',
    object_etag     TEXT,
    event_time_start TEXT,
    event_time_end  TEXT,
    uploaded_at     TEXT NOT NULL DEFAULT (datetime('now')),
    extracted_text_key TEXT,
    ocr_text_key    TEXT,
    transcript_key  TEXT,
    preview_key     TEXT,
    is_key_evidence BOOLEAN NOT NULL DEFAULT 0,
    tags            TEXT NOT NULL DEFAULT '[]',
    metadata        TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS incident (
    id              TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL REFERENCES workspace(id),
    title           TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'open',
    summary_md      TEXT,
    narrative_md    TEXT,
    allegation_tags TEXT NOT NULL DEFAULT '[]',
    incident_time_start TEXT,
    incident_time_end   TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS packet (
    id              TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL REFERENCES workspace(id),
    packet_type     TEXT NOT NULL DEFAULT 'investigation',
    status          TEXT NOT NULL DEFAULT 'draft',
    title           TEXT NOT NULL,
    target_name     TEXT,
    description_md  TEXT,
    settings        TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS draft (
    id              TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL REFERENCES workspace(id),
    incident_id     TEXT,
    packet_id       TEXT,
    draft_type      TEXT NOT NULL DEFAULT 'summary',
    status          TEXT NOT NULL DEFAULT 'draft',
    title           TEXT NOT NULL,
    body_md         TEXT,
    created_by      TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS custody_event (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id    TEXT NOT NULL REFERENCES workspace(id),
    evidence_id     TEXT,
    event_type      TEXT NOT NULL,
    actor_id        TEXT,
    actor_user_id   TEXT,
    actor_agent     TEXT,
    subject_kind    TEXT,
    subject_id      TEXT,
    detail          TEXT NOT NULL DEFAULT '{}',
    details         TEXT NOT NULL DEFAULT '{}',
    occurred_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS export_artifact (
    id              TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL REFERENCES workspace(id),
    kind            TEXT NOT NULL DEFAULT 'packet',
    title           TEXT NOT NULL DEFAULT 'export',
    packet_id       TEXT,
    draft_id        TEXT,
    format          TEXT NOT NULL DEFAULT 'zip',
    object_bucket   TEXT NOT NULL DEFAULT 'exports',
    object_key      TEXT NOT NULL,
    sha256          TEXT NOT NULL DEFAULT '',
    file_size_bytes INTEGER,
    size_bytes      INTEGER,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS incident_evidence (
    incident_id TEXT NOT NULL,
    evidence_id TEXT NOT NULL,
    sort_order  INTEGER DEFAULT 0,
    note        TEXT,
    added_at    TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (incident_id, evidence_id)
);

CREATE TABLE IF NOT EXISTS citation_anchor (
    id              TEXT PRIMARY KEY,
    workspace_id    TEXT,
    evidence_id     TEXT,
    citation_kind   TEXT,
    page_number     INTEGER,
    start_offset    INTEGER,
    end_offset      INTEGER,
    snippet         TEXT,
    bbox            TEXT,
    text_quote      TEXT,
    transcript_start_ms INTEGER,
    transcript_end_ms   INTEGER,
    url             TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS draft_citation (
    id        TEXT PRIMARY KEY,
    draft_id  TEXT NOT NULL,
    anchor_id TEXT NOT NULL,
    kind      TEXT NOT NULL DEFAULT 'reference',
    label     TEXT,
    selector  TEXT,
    note      TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (draft_id, anchor_id, selector)
);

CREATE TABLE IF NOT EXISTS packet_exhibit (
    id            TEXT PRIMARY KEY,
    packet_id     TEXT NOT NULL,
    evidence_id   TEXT NOT NULL,
    exhibit_label TEXT,
    exhibit_title TEXT,
    sort_order    INTEGER NOT NULL DEFAULT 0,
    notes_md      TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (packet_id, evidence_id)
);
"""

_db_ready = False


async def _init_db():
    global _db_ready
    if _db_ready:
        return
    async with engine.begin() as conn:
        for tbl in ["draft_citation", "citation_anchor", "packet_exhibit", "incident_evidence",
                     "custody_event", "export_artifact", "draft", "packet", "evidence_item",
                     "incident", "app_user", "workspace"]:
            await conn.execute(text(f"DROP TABLE IF EXISTS {tbl}"))
        for stmt in DDL.split(";"):
            stmt = stmt.strip()
            if stmt:
                await conn.execute(text(stmt))
        await conn.execute(text(
            "INSERT OR IGNORE INTO workspace (id, name, slug) VALUES (:id, :name, :slug)"
        ), {"id": str(WS_A_ID), "name": "Workspace A", "slug": "ws-a"})
        await conn.execute(text(
            "INSERT OR IGNORE INTO workspace (id, name, slug) VALUES (:id, :name, :slug)"
        ), {"id": str(WS_B_ID), "name": "Workspace B", "slug": "ws-b"})
        await conn.execute(text(
            "INSERT OR IGNORE INTO app_user (id, workspace_id, email, display_name, role, is_active) "
            "VALUES (:id, :wid, :email, :name, :role, 1)"
        ), {"id": str(USER_A_ID), "wid": str(WS_A_ID), "email": "alice@example.com", "name": "Alice", "role": "admin"})
        await conn.execute(text(
            "INSERT OR IGNORE INTO app_user (id, workspace_id, email, display_name, role, is_active) "
            "VALUES (:id, :wid, :email, :name, :role, 1)"
        ), {"id": str(USER_B_ID), "wid": str(WS_B_ID), "email": "bob@example.com", "name": "Bob", "role": "member"})
        await conn.execute(text(
            "INSERT OR IGNORE INTO app_user (id, workspace_id, email, display_name, role, is_active) "
            "VALUES (:id, :wid, :email, :name, :role, 0)"
        ), {"id": str(USER_INACTIVE_ID), "wid": str(WS_A_ID), "email": "inactive@example.com", "name": "Gone", "role": "member"})
    _db_ready = True


async def _override_get_db():
    await _init_db()
    async with TestSession() as session:
        yield session


def _make_app():
    import api.app.services.nats_jobs as nj
    from api.app.main import app

    app.dependency_overrides[get_db] = _override_get_db

    async def _noop_publish(**kwargs):
        return uuid4()

    async def _noop_stream():
        pass

    nj.publish_job = _noop_publish
    nj.ensure_stream = _noop_stream

    # Disable the lifespan (NATS connect) for tests
    app.router.lifespan_context = None
    return app


def token_for(user_id: UUID, workspace_id: UUID, email: str, role: str = "member") -> str:
    return create_access_token({
        "sub": str(user_id),
        "workspace_id": str(workspace_id),
        "email": email,
        "role": role,
    })


TOKEN_A = token_for(USER_A_ID, WS_A_ID, "alice@example.com", "admin")
TOKEN_B = token_for(USER_B_ID, WS_B_ID, "bob@example.com", "member")

_app = _make_app()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=_app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def auth_a():
    return {"Authorization": f"Bearer {TOKEN_A}"}


@pytest.fixture
def auth_b():
    return {"Authorization": f"Bearer {TOKEN_B}"}
