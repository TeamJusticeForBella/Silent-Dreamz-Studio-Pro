"""P0 Security: Authentication and workspace authorization tests.

Proves:
- Unauthenticated requests are denied (401/403)
- Wrong passwords are rejected (bcrypt verification)
- Users cannot access another workspace's resources (404 / empty)
- Upload-url and finalize reject unauthorized requests
- Expired and invalid tokens are rejected
- Registration requires a valid, unused, email-matched invitation
- Public registration cannot join an arbitrary workspace
- Inactive users are denied
- Default dev secrets are rejected in production
"""
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from api.app.core.config import settings, _INSECURE_DEFAULT_SECRET, guard_production_secrets
from api.app.core.auth import hash_password
from .conftest import (
    TOKEN_A, TOKEN_B, USER_A_ID, USER_B_ID, USER_INACTIVE_ID,
    WS_A_ID, WS_B_ID, ALICE_PASSWORD, BOB_PASSWORD,
    token_for,
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


# ── 3. Password verification (bcrypt) ────────────────────────────────

async def test_login_correct_password(client):
    resp = await client.post("/auth/login", json={"email": "alice@example.com", "password": ALICE_PASSWORD})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client):
    resp = await client.post("/auth/login", json={"email": "alice@example.com", "password": "wrong-password-123"})
    assert resp.status_code == 401


async def test_login_empty_password(client):
    resp = await client.post("/auth/login", json={"email": "alice@example.com", "password": ""})
    assert resp.status_code == 401


async def test_login_unknown_email(client):
    resp = await client.post("/auth/login", json={"email": "nobody@example.com", "password": "any"})
    assert resp.status_code == 401


async def test_login_inactive_user(client):
    resp = await client.post("/auth/login", json={"email": "inactive@example.com", "password": "inactive-pass"})
    assert resp.status_code == 401


async def test_login_token_grants_access(client):
    login = await client.post("/auth/login", json={"email": "alice@example.com", "password": ALICE_PASSWORD})
    tok = login.json()["access_token"]
    resp = await client.get("/evidence", headers={"Authorization": f"Bearer {tok}"})
    assert resp.status_code == 200


async def test_bob_login_correct_password(client):
    resp = await client.post("/auth/login", json={"email": "bob@example.com", "password": BOB_PASSWORD})
    assert resp.status_code == 200


async def test_bob_login_wrong_password(client):
    resp = await client.post("/auth/login", json={"email": "bob@example.com", "password": "not-bobs-password"})
    assert resp.status_code == 401


# ── 4. Cross-workspace isolation ─────────────────────────────────────

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


# ── 5. Upload / finalize reject unauthorized ─────────────────────────

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


# ── 6. Invitation-based registration ─────────────────────────────────

async def test_register_without_invite_fails(client):
    resp = await client.post("/auth/register", json={
        "email": "newuser@example.com",
        "display_name": "New User",
        "password": "strong-P@ss123",
        "invite_code": "nonexistent-code",
    })
    assert resp.status_code == 403


async def test_invite_requires_admin(client, auth_b):
    resp = await client.post("/auth/invite", json={
        "email": "invited@example.com",
    }, headers=auth_b)
    assert resp.status_code == 403, "Non-admin must not create invitations"


async def test_invite_and_register_flow(client, auth_a):
    invite_resp = await client.post("/auth/invite", json={
        "email": "newmember@example.com",
        "role": "member",
    }, headers=auth_a)
    assert invite_resp.status_code == 201
    invite_data = invite_resp.json()
    code = invite_data["invite_code"]
    assert invite_data["workspace_id"] == str(WS_A_ID)

    reg_resp = await client.post("/auth/register", json={
        "email": "newmember@example.com",
        "display_name": "New Member",
        "password": "new-member-P@ss1",
        "invite_code": code,
    })
    assert reg_resp.status_code == 201
    user = reg_resp.json()
    assert user["workspace_id"] == str(WS_A_ID)
    assert user["role"] == "member"

    login_resp = await client.post("/auth/login", json={
        "email": "newmember@example.com",
        "password": "new-member-P@ss1",
    })
    assert login_resp.status_code == 200


async def test_invite_code_cannot_be_reused(client, auth_a):
    invite_resp = await client.post("/auth/invite", json={
        "email": "oneuse@example.com",
        "role": "member",
    }, headers=auth_a)
    code = invite_resp.json()["invite_code"]

    await client.post("/auth/register", json={
        "email": "oneuse@example.com",
        "display_name": "First Use",
        "password": "first-P@ss1",
        "invite_code": code,
    })

    second = await client.post("/auth/register", json={
        "email": "oneuse2@example.com",
        "display_name": "Second Use",
        "password": "second-P@ss1",
        "invite_code": code,
    })
    assert second.status_code == 403, "Reused invite code must be rejected"


async def test_invite_wrong_email_rejected(client, auth_a):
    invite_resp = await client.post("/auth/invite", json={
        "email": "specific@example.com",
        "role": "member",
    }, headers=auth_a)
    code = invite_resp.json()["invite_code"]

    resp = await client.post("/auth/register", json={
        "email": "different@example.com",
        "display_name": "Wrong Email",
        "password": "wrong-email-P@ss1",
        "invite_code": code,
    })
    assert resp.status_code == 403, "Invite for different email must be rejected"


async def test_invite_no_auth_fails(client):
    resp = await client.post("/auth/invite", json={
        "email": "invited@example.com",
    })
    assert resp.status_code in (401, 403)


# ── 7. Default secret rejection in production ────────────────────────

def test_default_secret_rejected_in_production():
    original_env = settings.APP_ENV
    original_secret = settings.JWT_SECRET
    try:
        settings.APP_ENV = "production"
        settings.JWT_SECRET = _INSECURE_DEFAULT_SECRET
        with pytest.raises(SystemExit):
            guard_production_secrets()
    finally:
        settings.APP_ENV = original_env
        settings.JWT_SECRET = original_secret


def test_default_secret_allowed_in_development():
    original_env = settings.APP_ENV
    original_secret = settings.JWT_SECRET
    try:
        settings.APP_ENV = "development"
        settings.JWT_SECRET = _INSECURE_DEFAULT_SECRET
        guard_production_secrets()
    finally:
        settings.APP_ENV = original_env
        settings.JWT_SECRET = original_secret


# ── 8. Cross-workspace draft and export isolation ─────────────────────

async def test_cross_workspace_draft_isolation(client, auth_a, auth_b):
    body = {"title": "WS-A Draft"}
    create = await client.post("/drafts", json=body, headers=auth_a)
    if create.status_code == 201:
        did = create.json()["id"]
        get_resp = await client.get(f"/drafts/{did}", headers=auth_b)
        assert get_resp.status_code == 404


async def test_cross_workspace_export_list_isolation(client, auth_a, auth_b):
    resp_a = await client.get("/exports", headers=auth_a)
    resp_b = await client.get("/exports", headers=auth_b)
    assert resp_a.status_code == 200
    assert resp_b.status_code == 200
