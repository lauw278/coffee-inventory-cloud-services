# Coffee Inventory Management System — Cloud Services Checkpoint

A small Indonesian-language inventory CRUD app for coffee products. It demonstrates a web UI, REST API, PostgreSQL persistence, Dockerfile, Docker Compose, environment configuration, health checks, logs, and input validation.

## Architecture

Browser → Flask web/API container → PostgreSQL container → named Docker volume `postgres-data`.

Both services communicate over the private Compose network `app-net`. The web container exposes port 5000 by default. PostgreSQL is not published to the host.

## Requirements

- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose plugin (Linux)
- A terminal (PowerShell on Windows is fine)

## Run locally

1. Copy `.env.example` to `.env`.
   - Windows PowerShell: `Copy-Item .env.example .env`
   - macOS/Linux: `cp .env.example .env`
2. For a real deployment, change `POSTGRES_PASSWORD` in `.env` to a strong local secret. Do not commit `.env`.
3. Start services from this folder:

   ```bash
   docker compose up --build -d
   ```

4. Open `http://localhost:5000`.
5. Check service status and health:

   ```bash
   docker compose ps
   curl http://localhost:5000/health
   docker compose logs web
   docker compose logs db
   ```

   In PowerShell, `curl` may be an alias; `Invoke-RestMethod http://localhost:5000/health` also works.

## API examples

List: `GET /api/items`

Create:
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Arabika Gayo","category":"Biji kopi","quantity":12,"unit_price":145000}'
```

Invalid input test (must return HTTP 400):
```bash
curl -i -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Robusta","category":"Biji kopi","quantity":-2,"unit_price":90000}'
```

Update: `PUT /api/items/1` with JSON body fields `name`, `category`, `quantity`, `unit_price`.

Delete: `DELETE /api/items/1`.

## Demonstrate persistent storage

1. Add an item in the UI.
2. Run `docker compose down` (do **not** use `-v`).
3. Run `docker compose up -d`.
4. Refresh the UI. The item should remain because the named volume persists.
5. `docker compose down -v` deletes the database volume and data. Only do this if you intentionally want a clean reset.

## Demonstrate containerization and networking

- `docker compose images` — show built/downloaded images.
- `docker compose ps` — show running containers, ports, and health status.
- `docker network ls` — show the Compose network.
- `docker volume ls` — show the persistent volume.
- `docker compose logs --tail=50 web` — show application logs.
- `docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"` may require shell/environment adjustments in PowerShell; use the variable values from `.env`.

## Access control and security discussion

This checkpoint app has a **shared inventory**, not per-user private records. Therefore row-level security (RLS) isolation between two end users is not applicable to this chosen scope; do not claim RLS has been implemented. The database is only reachable on the internal Compose network, not directly published to the host. The app uses parameterized SQL queries and validates input. For production, add authentication/authorization, use a dedicated database role with only required permissions, manage secrets securely, and consider TLS, backups, and migrations. The example `.env` password is for local demonstration only.

## Cloud plan (for presentation)

The demo runs locally in Docker Compose. A suitable next step is to deploy the web container to a managed container service and use a managed PostgreSQL database, configure secrets in the platform's secret manager, enable HTTPS, and set up logs/monitoring. Exact cloud provider can be selected based on course material and budget.

## Troubleshooting

- **Port 5000 is in use:** set `WEB_PORT=5001` in `.env`, then run `docker compose up -d`.
- **Web service unhealthy / database unavailable:** run `docker compose ps` and `docker compose logs db web`; confirm `.env` values and wait for PostgreSQL health check.
- **App does not open:** confirm Docker Desktop is running and use `http://localhost:5000` (or your chosen `WEB_PORT`).
- **Need to reset demo data:** `docker compose down -v` removes persistent data. Use carefully.

## Week 1–7 mapping (adapt to your lecturer's exact slide terminology)

- Week 1: cloud computing concepts and service deployment discussion.
- Week 2: Git/repository workflow and Linux/container command line.
- Week 3: HTTP request/response and REST API endpoints.
- Week 4: virtualization/container concepts.
- Week 5: Dockerfile and image build.
- Week 6: Docker Compose, service communication, health checks, volumes.
- Week 7: relational database, schema, validation and access-control discussion.

Verify this mapping against your actual LMS slides; the assignment PDF names these topics but does not give the detailed week-by-week lecture content.
https://www.canva.com/design/DAHYhh_PB2c/bnIFaABKBOL88H4lNTTfag/edit
