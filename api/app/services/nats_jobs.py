import json
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..core.clients import get_jetstream

STREAM_NAME = "BCC_JOBS"


async def ensure_stream():
    js = await get_jetstream()
    try:
        await js.find_stream_name_by_subject("bcc.jobs.>")
    except Exception:
        await js.add_stream(
            name=STREAM_NAME,
            subjects=["bcc.jobs.>", "bcc.events.>", "bcc.dlq.>"],
            retention="workqueue",
            max_age=86400 * 7 * 1_000_000_000,
        )


async def publish_job(
    *,
    subject: str,
    kind: str,
    workspace_id: UUID,
    payload: dict,
    requested_by: str = "api",
    parent_job_id: UUID | None = None,
    priority: int = 50,
) -> UUID:
    js = await get_jetstream()
    job_id = uuid4()
    envelope = {
        "job_id": str(job_id),
        "workspace_id": str(workspace_id),
        "kind": kind,
        "priority": priority,
        "attempt": 1,
        "max_attempts": 5,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "trace": {
            "correlation_id": str(uuid4()),
            "parent_job_id": str(parent_job_id) if parent_job_id else None,
            "requested_by": requested_by,
            "actor": "API",
        },
        "payload": payload,
    }
    await js.publish(subject, json.dumps(envelope).encode())
    return job_id
