"""Priority 2: Authentication and workspace authorization tests.

Proves:
- Unauthenticated requests are denied (401)
- Users cannot access another workspace's resources (404 / empty)
- Upload-url and finalize reject unauthorized requests
- Expired and invalid tokens are rejected
"""
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from api.app.core.config import settings
from .conftest import (
    TOKEN_A, TOKEN_B, USER_A_ID, USER_B_ID, USER_INACTIVE_ID,
    WS_A_ID, WS_B_ID, token_for,
)

pytestmark = pytest.mark.asyncio


# ── Helper ────────────────────────────────────────────────────────────

PROTECTED_ENDPOINTS = [
    ("GET", "/evidence"),
    ("POST", "/evidence"),
    ("GET", "/incidents"),
    ("POST", "/incidents"),
    ("GET", "/packets"),
    ("POST", "/packets"),
    ("GET", "/drafts"),
    ("POST", "/drafts"),
    ("GET", "/exports"),
    ("GET", "/search?q=test"),
    ("POST", "/citations"),
]


# ── 1. Unauthenticated requests are denied ───────────────────────────

@pytest.mark.parametrize("method,path", PROTECTED_ENDPOINTS)
async def test_no_token_is_rejected(client, method, path):
    resp = await client.request(method, path)
    assert resp.status_code in (401, 403), f"{method} {path} returned {resp.status_code}, expected 401 or 403"


async def test_health_is_public(client):
    resp = await client.get("/health")
    assert resp.status_code == 200


# ── 2. Invalid / expired tokens are rejected ─────────────────────────

async def test_garbage_token(client):
    resp = await client.get("/evidence", headers={"Authorization": "Bearer garbage.token.here"})
    assert resp.status_code in (401, 403)


async def test_expired_token(client):
    expired = jwt.encode(
        {
            "sub": str(USER_A_ID),
            "workspace_id": str(WS_A_ID),
            "email": "alice@example.com",
            "role": "admin",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    resp = await client.get("/evidence", headers={"Authorization": f"Bearer {expired}"})
    assert resp.status_code in (401, 403)


async def test_wrong_secret_token(client):
    bad = jwt.encode(
        {
            "sub": str(USER_A_ID),
            "workspace_id": str(WS_A_ID),
            "email": "alice@example.com",
            "role": "admin",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        "wrong-secret-key",
        algorithm="HS256",
    )
    resp = await client.get("/evidence", headers={"Authorization": f"Bearer {bad}"})
    assert resp.status_code in (401, 403)


async def test_inactive_user_denied(client):
    tok = token_for(USER_INACTIVE_ID, WS_A_ID, "inactive@example.com")
    resp = await client.get("/evidence", headers={"Authorization": f"Bearer {tok}"})
    assert resp.status_code == 401


async def test_nonexistent_user_denied(client):
    fake_id = uuid4()
    tok = token_for(fake_id, WS_A_ID, "fake@example.com")
    resp = await client.get("/evidence", headers={"Authorization": f"Bearer {tok}"})
    assert resp.status_code == 401


# ── 3. Cross-workspace isolation ─────────────────────────────────────

async def test_user_a_creates_evidence(client, auth_a):
    body = {
        "title": "WS-A Document",
        "evidence_type": "pdf",
        "sha256": "a" * 64,
    }
    resp = await client.post("/evidence", json=body, headers=auth_a)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "WS-A Document"
    return data["id"]


async def test_user_b_cannot_see_ws_a_evidence(client, auth_a, auth_b):
    body = {
        "title": "WS-A Secret",
        "evidence_type": "pdf",
        "sha256": "b" * 64,
    }
    create = await client.post("/evidence", json=body, headers=auth_a)
    assert create.status_code == 201
    eid = create.json()["id"]

    get_resp = await client.get(f"/evidence/{eid}", headers=auth_b)
    assert get_resp.status_code == 404, "User B must not access Workspace A evidence"


async def test_user_b_list_excludes_ws_a(client, auth_a, auth_b):
    body = {
        "title": "WS-A Listed Item",
        "evidence_type": "other",
        "sha256": "c" * 64,
    }
    await client.post("/evidence", json=body, headers=auth_a)

    resp = await client.get("/evidence", headers=auth_b)
    assert resp.status_code == 200
    items = resp.json()["items"]
    for item in items:
        assert "WS-A" not in item["title"], "WS-B list must not contain WS-A items"


async def test_cross_workspace_incident_isolation(client, auth_a, auth_b):
    body = {"title": "WS-A Incident"}
    create = await client.post("/incidents", json=body, headers=auth_a)
    assert create.status_code == 201
    iid = create.json()["id"]

    get_resp = await client.get(f"/incidents/{iid}", headers=auth_b)
    assert get_resp.status_code == 404


async def test_cross_workspace_packet_isolation(client, auth_a, auth_b):
    body = {"title": "WS-A Packet", "packet_type": "other"}
    create = await client.post("/packets", json=body, headers=auth_a)
    assert create.status_code == 201
    pid = create.json()["id"]

    get_resp = await client.get(f"/packets/{pid}", headers=auth_b)
    assert get_resp.status_code == 404


async def test_cross_workspace_patch_blocked(client, auth_a, auth_b):
    body = {
        "title": "WS-A Patchable",
        "evidence_type": "pdf",
        "sha256": "d" * 64,
    }
    create = await client.post("/evidence", json=body, headers=auth_a)
    eid = create.json()["id"]

    patch_resp = await client.patch(
        f"/evidence/{eid}", json={"title": "Hijacked"}, headers=auth_b,
    )
    assert patch_resp.status_code == 404, "Cross-workspace patch must be blocked"


# ── 4. Upload / finalize reject unauthorized ─────────────────────────

async def test_upload_url_no_token(client):
    eid = uuid4()
    resp = await client.post(
        f"/evidence/{eid}/upload-url",
        json={"filename": "test.pdf"},
    )
    assert resp.status_code in (401, 403)


async def test_finalize_no_token(client):
    eid = uuid4()
    resp = await client.post(
        f"/evidence/{eid}/finalize",
        json={"object_bucket": "evidence", "object_key": "x"},
    )
    assert resp.status_code in (401, 403)


# ── 5. Auth login endpoint ───────────────────────────────────────────

async def test_login_valid_user(client):
    resp = await client.post("/auth/login", json={"email": "alice@example.com", "password": "any"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_unknown_email(client):
    resp = await client.post("/auth/login", json={"email": "nobody@example.com", "password": "any"})
    assert resp.status_code == 401


async def test_login_inactive_user(client):
    resp = await client.post("/auth/login", json={"email": "inactive@example.com", "password": "any"})
    assert resp.status_code == 401


async def test_login_empty_password(client):
    resp = await client.post("/auth/login", json={"email": "alice@example.com", "password": ""})
    assert resp.status_code == 401


# ── 6. Token from login works on protected endpoints ─────────────────

async def test_login_token_grants_access(client):
    login = await client.post("/auth/login", json={"email": "alice@example.com", "password": "pw"})
    tok = login.json()["access_token"]
    resp = await client.get("/evidence", headers={"Authorization": f"Bearer {tok}"})
    assert resp.status_code == 200
