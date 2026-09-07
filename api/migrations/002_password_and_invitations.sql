-- Migration 002: Add password hashing and invitation-based registration
-- Applies to both Postgres and SQLite (via compatible syntax)

-- 1. Add password_hash column to app_user
ALTER TABLE app_user ADD COLUMN password_hash TEXT;

-- 2. Create workspace_invitation table for owner-approved membership
CREATE TABLE IF NOT EXISTS workspace_invitation (
    id          TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL REFERENCES workspace(id),
    email       TEXT NOT NULL,
    role        TEXT NOT NULL DEFAULT 'member',
    invite_code TEXT NOT NULL UNIQUE,
    created_by  TEXT REFERENCES app_user(id),
    used_at     TEXT,
    expires_at  TEXT,
    created_at  TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE INDEX IF NOT EXISTS idx_invitation_code ON workspace_invitation(invite_code);
CREATE INDEX IF NOT EXISTS idx_invitation_email ON workspace_invitation(email);
