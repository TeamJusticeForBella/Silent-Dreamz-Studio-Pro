#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# Bella Command Center – Bootstrap Script
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Defaults (override via environment)
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5432}"
PG_USER="${PG_USER:-bcc}"
PG_DB="${PG_DB:-bcc}"
PGPASSWORD="${PGPASSWORD:-bcc}"
export PGPASSWORD

OPENSEARCH_URL="${OPENSEARCH_URL:-http://localhost:9200}"
QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"

# ─────────────────────────────────────────────
# 1. Wait for Postgres
# ─────────────────────────────────────────────
echo ">>> Waiting for Postgres at ${PG_HOST}:${PG_PORT}..."
until pg_isready -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -q; do
  sleep 2
done
echo ">>> Postgres is ready."

# ─────────────────────────────────────────────
# 2. Wait for OpenSearch
# ─────────────────────────────────────────────
echo ">>> Waiting for OpenSearch at ${OPENSEARCH_URL}..."
until curl -sf "${OPENSEARCH_URL}/_cluster/health" >/dev/null 2>&1; do
  sleep 2
done
echo ">>> OpenSearch is ready."

# ─────────────────────────────────────────────
# 3. Wait for Qdrant
# ─────────────────────────────────────────────
echo ">>> Waiting for Qdrant at ${QDRANT_URL}..."
until curl -sf "${QDRANT_URL}/healthz" >/dev/null 2>&1; do
  sleep 2
done
echo ">>> Qdrant is ready."

# ─────────────────────────────────────────────
# 4. Apply Postgres DDL
# ─────────────────────────────────────────────
echo ">>> Applying db/001_init.sql..."
psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" \
  -f "${SCRIPT_DIR}/../db/001_init.sql"
echo ">>> Postgres DDL applied."

# ─────────────────────────────────────────────
# 5. Create OpenSearch indices (skip if exists)
# ─────────────────────────────────────────────
declare -a OS_INDICES=(
  "bcc-evidence-v1"
  "bcc-incidents-v1"
  "bcc-drafts-v1"
  "bcc-packets-v1"
)

for idx in "${OS_INDICES[@]}"; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${OPENSEARCH_URL}/${idx}")
  if [ "$HTTP_CODE" = "200" ]; then
    echo ">>> OpenSearch index '${idx}' already exists – skipping."
  else
    echo ">>> Creating OpenSearch index '${idx}'..."
    curl -s -X PUT "${OPENSEARCH_URL}/${idx}" \
      -H "Content-Type: application/json" \
      -d @"${SCRIPT_DIR}/opensearch/${idx}.json"
    echo ""
    echo ">>> Index '${idx}' created."
  fi
done

# ─────────────────────────────────────────────
# 6. Create Qdrant collection (skip if exists)
# ─────────────────────────────────────────────
QDRANT_COLLECTION="bcc_evidence_chunks_v1"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${QDRANT_URL}/collections/${QDRANT_COLLECTION}")
if [ "$HTTP_CODE" = "200" ]; then
  echo ">>> Qdrant collection '${QDRANT_COLLECTION}' already exists – skipping."
else
  echo ">>> Creating Qdrant collection '${QDRANT_COLLECTION}'..."
  curl -s -X PUT "${QDRANT_URL}/collections/${QDRANT_COLLECTION}" \
    -H "Content-Type: application/json" \
    -d @"${SCRIPT_DIR}/qdrant/create-collection.json"
  echo ""
  echo ">>> Collection '${QDRANT_COLLECTION}' created."
fi

# ─────────────────────────────────────────────
# 7. Create Qdrant payload indexes
# ─────────────────────────────────────────────
echo ">>> Creating Qdrant payload indexes..."
PAYLOAD_INDEXES=$(cat "${SCRIPT_DIR}/qdrant/payload-indexes.json")
LENGTH=$(echo "$PAYLOAD_INDEXES" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")

for (( i=0; i<LENGTH; i++ )); do
  FIELD_NAME=$(echo "$PAYLOAD_INDEXES" | python3 -c "import sys,json; print(json.load(sys.stdin)[$i]['field_name'])")
  FIELD_SCHEMA=$(echo "$PAYLOAD_INDEXES" | python3 -c "import sys,json; print(json.load(sys.stdin)[$i]['field_schema'])")
  echo ">>>   Creating index on '${FIELD_NAME}' (${FIELD_SCHEMA})..."
  curl -s -X PUT "${QDRANT_URL}/collections/${QDRANT_COLLECTION}/index" \
    -H "Content-Type: application/json" \
    -d "{\"field_name\":\"${FIELD_NAME}\",\"field_schema\":\"${FIELD_SCHEMA}\"}"
  echo ""
done
echo ">>> Qdrant payload indexes created."

# ─────────────────────────────────────────────
# 8. Seed admin user
# ─────────────────────────────────────────────
echo ">>> Seeding admin user admin@local..."
psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" <<'SQL'
INSERT INTO app_user (workspace_id, email, display_name, role)
VALUES ('00000000-0000-0000-0000-000000000001', 'admin@local', 'Admin', 'admin')
ON CONFLICT (workspace_id, email) DO NOTHING;
SQL
echo ">>> Admin user seeded."

echo ""
echo "========================================="
echo "  Bella Command Center bootstrap complete"
echo "========================================="
