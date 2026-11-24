#!/usr/bin/env bash
# Idempotent first-boot DB bootstrap for Tera.
# Creates enum types and base tables before running migrations; safe to re-run.
# Never deletes data or volumes.
set -euo pipefail
cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-config.env}"
FILES="${COMPOSE_FILES:-docker-compose.yml docker-compose.prod.yml}"
# shellcheck disable=SC2206
FILE_ARGS=($FILES)
COMPOSE=(docker compose --env-file "$ENV_FILE")
for f in "${FILE_ARGS[@]}"; do COMPOSE+=(-f "$f"); done
if [ -f .secrets ]; then COMPOSE+=(--env-file .secrets); fi

"${COMPOSE[@]}" up -d db redis
for i in $(seq 1 20); do
  if "${COMPOSE[@]}" exec -T db sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"' >/dev/null 2>&1; then break; fi
  [ "$i" -eq 20 ] && { echo "DB not ready" >&2; exit 1; }
  sleep 2
done

"${COMPOSE[@]}" run --rm --no-deps back python -c '
import app.models, app.inventory_models
from app.db import engine, create_db_and_tables
from sqlalchemy import Enum
for table in app.models.SQLModel.metadata.tables.values():
    for col in table.columns:
        t = col.type
        if isinstance(t, Enum) and getattr(t, "create_type", True) is False:
            t.create(engine, checkfirst=True)
create_db_and_tables()
'
"${COMPOSE[@]}" run --rm --no-deps back python -m app.migrate
"${COMPOSE[@]}" run --rm --no-deps back python -m app.migrate --sync-idempotent
echo "Database bootstrap complete."
