"""Priority 3: SHA-256 chain-of-custody and audit logging tests.

Uses synthetic fixtures only — no real Bella data.
"""
import hashlib

import pytest
from sqlalchemy import text

from .conftest import TOKEN_A, WS_A_ID, TestSession

pytestmark = pytest.mark.asyncio


async def _count_custody_events(workspace_id: str, subject_id: str | None = None) -> int:
    async with TestSession() as db:
        q = "SELECT COUNT(*) FROM custody_event WHERE workspace_id = :wid"
        params: dict = {"wid": workspace_id}
        if subject_id:
            q += " AND subject_id = :sid"
            params["sid"] = subject_id
        r = await db.execute(text(q), params)
        return r.scalar()


async def _get_custody_events(workspace_id: str, subject_id: str) -> list[dict]:
    async with TestSession() as db:
        r = await db.execute(
            text(
                "SELECT * FROM custody_event WHERE workspace_id = :wid AND subject_id = :sid "
                "ORDER BY id"
            ),
            {"wid": workspace_id, "sid": subject_id},
        )
        return [dict(row._mapping) for row in r.fetchall()]


# ── SHA-256 is recorded on evidence creation ──────────────────────────

async def test_sha256_stored_on_create(client, auth_a):
    synthetic_hash = hashlib.sha256(b"synthetic test data").hexdigest()
    body = {
        "title": "SHA256 Test Doc",
        "evidence_type": "pdf",
        "sha256": synthetic_hash,
    }
    resp = await client.post("/evidence", json=body, headers=auth_a)
    assert resp.status_code == 201
    data = resp.json()
    assert data["sha256"] == synthetic_hash, "SHA-256 must be preserved exactly"


async def test_sha256_returned_on_get(client, auth_a):
    h = hashlib.sha256(b"another synthetic document").hexdigest()
    create = await client.post("/evidence", json={
        "title": "SHA256 Retrieve",
        "evidence_type": "other",
        "sha256": h,
    }, headers=auth_a)
    eid = create.json()["id"]

    get = await client.get(f"/evidence/{eid}", headers=auth_a)
    assert get.status_code == 200
    assert get.json()["sha256"] == h


async def test_sha256_immutable_on_patch(client, auth_a):
    h = hashlib.sha256(b"immutable data").hexdigest()
    create = await client.post("/evidence", json={
        "title": "Immutable SHA",
        "evidence_type": "pdf",
        "sha256": h,
    }, headers=auth_a)
    eid = create.json()["id"]

    patch = await client.patch(
        f"/evidence/{eid}",
        json={"title": "Renamed"},
        headers=auth_a,
    )
    assert patch.status_code == 200
    assert patch.json()["sha256"] == h, "SHA-256 must not change on patch"


# ── Custody event logged on evidence creation ─────────────────────────

async def test_custody_event_on_evidence_create(client, auth_a):
    h = hashlib.sha256(b"custody test").hexdigest()
    resp = await client.post("/evidence", json={
        "title": "Custody Audit Item",
        "evidence_type": "other",
        "sha256": h,
    }, headers=auth_a)
    assert resp.status_code == 201
    eid = resp.json()["id"]

    events = await _get_custody_events(str(WS_A_ID), eid)
    assert len(events) >= 1, "At least one custody event expected"
    assert events[0]["event_type"] == "ingested"


# ── Custody event on incident link ────────────────────────────────────

async def test_custody_event_on_incident_link(client, auth_a):
    ev = await client.post("/evidence", json={
        "title": "Link Target",
        "evidence_type": "pdf",
        "sha256": "e" * 64,
    }, headers=auth_a)
    eid = ev.json()["id"]

    inc = await client.post("/incidents", json={"title": "Link Incident"}, headers=auth_a)
    iid = inc.json()["id"]

    link = await client.post(
        f"/incidents/{iid}/evidence",
        json={"evidence_id": eid, "sort_order": 0},
        headers=auth_a,
    )
    assert link.status_code == 200

    events = await _get_custody_events(str(WS_A_ID), eid)
    types = [e["event_type"] for e in events]
    assert "linked_incident" in types, "linked_incident custody event expected"


# ── Custody event on draft status change ──────────────────────────────

async def test_custody_event_on_draft_approve(client, auth_a):
    async with TestSession() as db:
        from uuid import uuid4
        did = str(uuid4())
        await db.execute(text(
            "INSERT INTO draft (id, workspace_id, draft_type, status, title) "
            "VALUES (:id, :wid, 'summary', 'draft', 'Test Draft')"
        ), {"id": did, "wid": str(WS_A_ID)})
        await db.commit()

    resp = await client.post(
        f"/drafts/{did}/status",
        json={"status": "approved", "note": "Looks good"},
        headers=auth_a,
    )
    assert resp.status_code == 200

    events = await _get_custody_events(str(WS_A_ID), did)
    types = [e["event_type"] for e in events]
    assert "draft_approved" in types


# ── Multiple custody events are append-only ───────────────────────────

async def test_custody_events_are_append_only(client, auth_a):
    h = hashlib.sha256(b"append only proof").hexdigest()
    create = await client.post("/evidence", json={
        "title": "Append Only Test",
        "evidence_type": "pdf",
        "sha256": h,
    }, headers=auth_a)
    eid = create.json()["id"]

    before = await _get_custody_events(str(WS_A_ID), eid)

    await client.patch(f"/evidence/{eid}", json={"title": "Renamed Again"}, headers=auth_a)

    after = await _get_custody_events(str(WS_A_ID), eid)
    assert len(after) >= len(before), "Custody events must never decrease (append-only)"


# ── Evidence SHA-256 distinct per item ────────────────────────────────

async def test_different_evidence_different_hashes(client, auth_a):
    h1 = hashlib.sha256(b"file one").hexdigest()
    h2 = hashlib.sha256(b"file two").hexdigest()
    assert h1 != h2

    r1 = await client.post("/evidence", json={
        "title": "File One", "evidence_type": "pdf", "sha256": h1,
    }, headers=auth_a)
    r2 = await client.post("/evidence", json={
        "title": "File Two", "evidence_type": "pdf", "sha256": h2,
    }, headers=auth_a)

    assert r1.json()["sha256"] != r2.json()["sha256"]
