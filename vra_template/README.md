# VRA Dash template

Create a new dashboard repository from this directory; do not run it as a shared multi-tenant platform. Copy `.env.example` to `.env`, set a **read-only** `DW_DSN`, then run `docker compose up --build`.

The application is an application factory (`vra_dashboard.app:create_app`). Data code accepts typed filters, aggregates in PostgreSQL, and caches DTO-shaped results only in Redis. `DW_REFRESH_MARKER` invalidates all prior keys after an ETL refresh. No DDL, write statement, or full fact-table extraction belongs in this template.

Run `pytest` for unit tests. Use `docker compose -f compose.integration.yaml up --build --abort-on-container-exit` for PostgreSQL/Redis integration. Record representative environment runs with `python benchmarks/run.py` and preserve the JSON report.
