-- Bella Command Center – Postgres 16 DDL
-- Applied automatically via docker-entrypoint-initdb.d

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ─────────────────────────────────────────────
-- ENUMS
-- ─────────────────────────────────────────────

DO $$ BEGIN
    CREATE TYPE evidence_type AS ENUM (
        'document','image','video','audio','email','chat_log','spreadsheet','other'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE draft_type AS ENUM (
        'summary','narrative','memo','report','letter','other'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE draft_status AS ENUM (
        'draft','review','approved','final','archived'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE packet_type AS ENUM (
        'investigation','discipline','termination','referral','closing','other'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE packet_status AS ENUM (
        'assembling','review','submitted','accepted','returned','archived'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE custody_event_type AS ENUM (
        'ingested','viewed','downloaded','exported','redacted','deleted','transferred','sealed'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE entity_type AS ENUM (
        'person','organization','location','vehicle','phone','email_addr','account','other'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE citation_kind AS ENUM (
        'quote','paraphrase','reference','exhibit'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ─────────────────────────────────────────────
-- TABLES
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS workspace (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    slug            TEXT NOT NULL UNIQUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS app_user (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    email           TEXT NOT NULL,
    display_name    TEXT,
    role            TEXT NOT NULL DEFAULT 'member',
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, email)
);

CREATE TABLE IF NOT EXISTS evidence_item (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    title           TEXT NOT NULL,
    evidence_type   evidence_type NOT NULL DEFAULT 'other',
    source_kind     TEXT,
    sha256          TEXT NOT NULL,
    object_key      TEXT NOT NULL,
    content_mime    TEXT,
    file_size_bytes BIGINT,
    tags            TEXT[] NOT NULL DEFAULT '{}',
    metadata        JSONB NOT NULL DEFAULT '{}',
    is_key_evidence BOOLEAN NOT NULL DEFAULT false,
    event_time_start TIMESTAMPTZ,
    event_time_end  TIMESTAMPTZ,
    uploaded_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS incident (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    title           TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'open',
    summary_md      TEXT,
    narrative_md    TEXT,
    allegation_tags TEXT[] NOT NULL DEFAULT '{}',
    incident_time_start TIMESTAMPTZ,
    incident_time_end   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS incident_evidence (
    incident_id     UUID NOT NULL REFERENCES incident(id) ON DELETE CASCADE,
    evidence_id     UUID NOT NULL REFERENCES evidence_item(id) ON DELETE CASCADE,
    added_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (incident_id, evidence_id)
);

CREATE TABLE IF NOT EXISTS entity (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    entity_type     entity_type NOT NULL,
    canonical_name  TEXT NOT NULL,
    aliases         TEXT[] NOT NULL DEFAULT '{}',
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS evidence_entity (
    evidence_id     UUID NOT NULL REFERENCES evidence_item(id) ON DELETE CASCADE,
    entity_id       UUID NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    confidence      REAL NOT NULL DEFAULT 1.0,
    context_snippet TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (evidence_id, entity_id)
);

CREATE TABLE IF NOT EXISTS packet (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    packet_type     packet_type NOT NULL DEFAULT 'investigation',
    status          packet_status NOT NULL DEFAULT 'assembling',
    title           TEXT NOT NULL,
    target_name     TEXT,
    description_md  TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS packet_exhibit (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    packet_id       UUID NOT NULL REFERENCES packet(id) ON DELETE CASCADE,
    evidence_id     UUID NOT NULL REFERENCES evidence_item(id) ON DELETE CASCADE,
    exhibit_label   TEXT,
    sort_order      INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS draft (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    incident_id     UUID REFERENCES incident(id) ON DELETE SET NULL,
    packet_id       UUID REFERENCES packet(id) ON DELETE SET NULL,
    draft_type      draft_type NOT NULL DEFAULT 'summary',
    status          draft_status NOT NULL DEFAULT 'draft',
    title           TEXT NOT NULL,
    body_md         TEXT,
    created_by      UUID REFERENCES app_user(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS citation_anchor (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id     UUID NOT NULL REFERENCES evidence_item(id) ON DELETE CASCADE,
    page_number     INT,
    start_offset    INT,
    end_offset      INT,
    snippet         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS draft_citation (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    draft_id        UUID NOT NULL REFERENCES draft(id) ON DELETE CASCADE,
    anchor_id       UUID NOT NULL REFERENCES citation_anchor(id) ON DELETE CASCADE,
    kind            citation_kind NOT NULL DEFAULT 'reference',
    label           TEXT,
    sort_order      INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS export_artifact (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    packet_id       UUID REFERENCES packet(id) ON DELETE SET NULL,
    draft_id        UUID REFERENCES draft(id) ON DELETE SET NULL,
    format          TEXT NOT NULL,
    object_key      TEXT NOT NULL,
    file_size_bytes BIGINT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS custody_event (
    id              BIGSERIAL PRIMARY KEY,
    workspace_id    UUID NOT NULL REFERENCES workspace(id),
    evidence_id     UUID NOT NULL REFERENCES evidence_item(id) ON DELETE CASCADE,
    event_type      custody_event_type NOT NULL,
    actor_id        UUID REFERENCES app_user(id) ON DELETE SET NULL,
    detail          JSONB NOT NULL DEFAULT '{}',
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─────────────────────────────────────────────
-- INDEXES – foreign keys
-- ─────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_app_user_workspace ON app_user(workspace_id);
CREATE INDEX IF NOT EXISTS idx_evidence_item_workspace ON evidence_item(workspace_id);
CREATE INDEX IF NOT EXISTS idx_incident_workspace ON incident(workspace_id);
CREATE INDEX IF NOT EXISTS idx_incident_evidence_evidence ON incident_evidence(evidence_id);
CREATE INDEX IF NOT EXISTS idx_entity_workspace ON entity(workspace_id);
CREATE INDEX IF NOT EXISTS idx_evidence_entity_entity ON evidence_entity(entity_id);
CREATE INDEX IF NOT EXISTS idx_packet_workspace ON packet(workspace_id);
CREATE INDEX IF NOT EXISTS idx_packet_exhibit_packet ON packet_exhibit(packet_id);
CREATE INDEX IF NOT EXISTS idx_packet_exhibit_evidence ON packet_exhibit(evidence_id);
CREATE INDEX IF NOT EXISTS idx_draft_workspace ON draft(workspace_id);
CREATE INDEX IF NOT EXISTS idx_draft_incident ON draft(incident_id);
CREATE INDEX IF NOT EXISTS idx_draft_packet ON draft(packet_id);
CREATE INDEX IF NOT EXISTS idx_draft_created_by ON draft(created_by);
CREATE INDEX IF NOT EXISTS idx_citation_anchor_evidence ON citation_anchor(evidence_id);
CREATE INDEX IF NOT EXISTS idx_draft_citation_draft ON draft_citation(draft_id);
CREATE INDEX IF NOT EXISTS idx_draft_citation_anchor ON draft_citation(anchor_id);
CREATE INDEX IF NOT EXISTS idx_export_artifact_workspace ON export_artifact(workspace_id);
CREATE INDEX IF NOT EXISTS idx_export_artifact_packet ON export_artifact(packet_id);
CREATE INDEX IF NOT EXISTS idx_export_artifact_draft ON export_artifact(draft_id);
CREATE INDEX IF NOT EXISTS idx_custody_event_workspace ON custody_event(workspace_id);
CREATE INDEX IF NOT EXISTS idx_custody_event_evidence ON custody_event(evidence_id);
CREATE INDEX IF NOT EXISTS idx_custody_event_actor ON custody_event(actor_id);

-- ─────────────────────────────────────────────
-- INDEXES – GIN on tags / metadata / time
-- ─────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_evidence_item_tags ON evidence_item USING GIN (tags);
CREATE INDEX IF NOT EXISTS idx_evidence_item_metadata ON evidence_item USING GIN (metadata);
CREATE INDEX IF NOT EXISTS idx_evidence_item_uploaded_at ON evidence_item(uploaded_at);
CREATE INDEX IF NOT EXISTS idx_evidence_item_event_time ON evidence_item(event_time_start, event_time_end);
CREATE INDEX IF NOT EXISTS idx_incident_allegation_tags ON incident USING GIN (allegation_tags);
CREATE INDEX IF NOT EXISTS idx_incident_created_at ON incident(created_at);
CREATE INDEX IF NOT EXISTS idx_custody_event_occurred_at ON custody_event(occurred_at);

-- ─────────────────────────────────────────────
-- TRIGGERS – set_updated_at
-- ─────────────────────────────────────────────

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_incident_updated_at ON incident;
CREATE TRIGGER trg_incident_updated_at
    BEFORE UPDATE ON incident
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_packet_updated_at ON packet;
CREATE TRIGGER trg_packet_updated_at
    BEFORE UPDATE ON packet
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_draft_updated_at ON draft;
CREATE TRIGGER trg_draft_updated_at
    BEFORE UPDATE ON draft
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ─────────────────────────────────────────────
-- SEED DATA
-- ─────────────────────────────────────────────

INSERT INTO workspace (id, name, slug)
VALUES ('00000000-0000-0000-0000-000000000001', 'Default Workspace', 'default')
ON CONFLICT (id) DO NOTHING;
