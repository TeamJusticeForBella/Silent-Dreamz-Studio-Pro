from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import text

from ..core.auth import create_access_token, hash_password, verify_password
from ..core.deps import CurrentUser, DBSession

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    display_name: str
    password: str
    invite_code: str


class UserResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    email: str
    display_name: str
    role: str


class InviteRequest(BaseModel):
    email: EmailStr
    role: str = "member"


class InviteResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    email: str
    role: str
    invite_code: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DBSession):
    if not body.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    result = await db.execute(
        text("SELECT id, workspace_id, email, role, password_hash FROM app_user WHERE email = :email AND is_active = true"),
        {"email": body.email},
    )
    row = result.mappings().first()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not row["password_hash"] or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token({
        "sub": str(row["id"]),
        "workspace_id": str(row["workspace_id"]),
        "email": row["email"],
        "role": row["role"],
    })
    return TokenResponse(access_token=token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: DBSession):
    inv = await db.execute(
        text(
            "SELECT id, workspace_id, email, role, used_at, expires_at FROM workspace_invitation "
            "WHERE invite_code = :code"
        ),
        {"code": body.invite_code},
    )
    invite = inv.mappings().first()
    if invite is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid invitation code",
        )

    if invite["used_at"] is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invitation already used",
        )

    if invite["expires_at"]:
        exp = invite["expires_at"]
        if isinstance(exp, str):
            exp = datetime.fromisoformat(exp)
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invitation has expired",
            )

    if invite["email"] != body.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invitation is for a different email address",
        )

    exists = await db.execute(
        text("SELECT 1 FROM app_user WHERE email = :email AND workspace_id = :wid"),
        {"email": body.email, "wid": str(invite["workspace_id"])},
    )
    if exists.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered in this workspace",
        )

    user_id = uuid4()
    pw_hash = hash_password(body.password)

    await db.execute(
        text(
            "INSERT INTO app_user (id, workspace_id, email, display_name, role, is_active, password_hash) "
            "VALUES (:id, :wid, :email, :name, :role, true, :pw_hash)"
        ),
        {
            "id": str(user_id),
            "wid": str(invite["workspace_id"]),
            "email": body.email,
            "name": body.display_name,
            "role": invite["role"],
            "pw_hash": pw_hash,
        },
    )

    await db.execute(
        text("UPDATE workspace_invitation SET used_at = :now WHERE id = :iid"),
        {"now": datetime.now(timezone.utc).isoformat(), "iid": str(invite["id"])},
    )
    await db.commit()

    return UserResponse(
        id=user_id,
        workspace_id=invite["workspace_id"],
        email=body.email,
        display_name=body.display_name,
        role=invite["role"],
    )


@router.post("/invite", response_model=InviteResponse, status_code=status.HTTP_201_CREATED)
async def create_invitation(body: InviteRequest, user: CurrentUser, db: DBSession):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace admins can create invitations",
        )

    import secrets
    invite_id = uuid4()
    code = secrets.token_urlsafe(32)

    await db.execute(
        text(
            "INSERT INTO workspace_invitation (id, workspace_id, email, role, invite_code, created_by) "
            "VALUES (:id, :wid, :email, :role, :code, :uid)"
        ),
        {
            "id": str(invite_id),
            "wid": str(user.workspace_id),
            "email": body.email,
            "role": body.role,
            "code": code,
            "uid": str(user.id),
        },
    )
    await db.commit()

    return InviteResponse(
        id=invite_id,
        workspace_id=user.workspace_id,
        email=body.email,
        role=body.role,
        invite_code=code,
    )
