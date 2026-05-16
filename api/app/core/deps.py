from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db


async def get_workspace_id(x_workspace_id: Annotated[str, Header()]) -> UUID:
    try:
        return UUID(x_workspace_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-Workspace-Id header")


DBSession = Annotated[AsyncSession, Depends(get_db)]
WorkspaceId = Annotated[UUID, Depends(get_workspace_id)]
