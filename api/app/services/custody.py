from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def log_custody_event(
    db: AsyncSession,
    *,
    workspace_id: UUID,
    event_type: str,
    subject_kind: str,
    subject_id: UUID,
    actor_user_id: UUID | None = None,
    actor_agent: str | None = None,
    details: dict | None = None,
) -> int:
    result = await db.execute(
        text("""
            INSERT INTO custody_event
                (workspace_id, event_type, subject_kind, subject_id,
                 actor_user_id, actor_agent, details)
            VALUES
                (:workspace_id, :event_type, :subject_kind, :subject_id,
                 :actor_user_id, :actor_agent, :details)
            RETURNING id
        """),
        {
            "workspace_id": str(workspace_id),
            "event_type": event_type,
            "subject_kind": subject_kind,
            "subject_id": str(subject_id),
            "actor_user_id": str(actor_user_id) if actor_user_id else None,
            "actor_agent": actor_agent,
            "details": details or {},
        },
    )
    row = result.fetchone()
    return row[0]
