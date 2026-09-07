from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import text

from ..core.auth import create_access_token
from ..core.deps import DBSession

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
    workspace_id: UUID
    password: str  # accepted but NOT stored yet


class UserResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    email: str
    display_name: str
    role: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DBSession):
    # NOTE: Password verification is deferred -- the app_user table has no
    # password column yet.  For this MVP any non-empty password is accepted
    # for an active user.  A real implementation MUST hash and verify.
    if not body.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password required",
        )

    result = await db.execute(
        text("SELECT id, workspace_id, email, role FROM app_user WHERE email = :email AND is_active = true"),
        {"email": body.email},
    )
    row = result.mappings().first()
    if row is None:
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
    # Check for duplicate email
    exists = await db.execute(
        text("SELECT 1 FROM app_user WHERE email = :email"),
        {"email": body.email},
    )
    if exists.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Verify the workspace exists
    ws = await db.execute(
        text("SELECT 1 FROM workspace WHERE id = :wid"),
        {"wid": str(body.workspace_id)},
    )
    if ws.first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace not found",
        )

    user_id = uuid4()
    # NOTE: password is NOT stored -- deferred until a password column and
    # hashing are added.
    await db.execute(
        text(
            "INSERT INTO app_user (id, workspace_id, email, display_name, role, is_active) "
            "VALUES (:id, :wid, :email, :name, 'member', true)"
        ),
        {
            "id": str(user_id),
            "wid": str(body.workspace_id),
            "email": body.email,
            "name": body.display_name,
        },
    )
    await db.commit()

    return UserResponse(
        id=user_id,
        workspace_id=body.workspace_id,
        email=body.email,
        display_name=body.display_name,
        role="member",
    )
