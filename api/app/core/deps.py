from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import AuthenticatedUser, get_current_user
from .database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]


def get_workspace_id(user: AuthenticatedUser = Depends(get_current_user)) -> UUID:
    """Server-resolved workspace -- never trust a client header."""
    return user.workspace_id


WorkspaceId = Annotated[UUID, Depends(get_workspace_id)]
