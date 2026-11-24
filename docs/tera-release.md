# Tera Release Status

## Summary

The Tera rebrand is release-ready as a **local Docker Compose deployment**. The full stack is running locally at `http://127.0.0.1:4202`; core restaurant workflows, browser UI, mobile layout and WebSocket connectivity were verified after a clean database bootstrap and a service restart.

**Public deployment was not performed.** No authorized target host, domain, DNS control, TLS certificate, SSH credentials or explicit publish approval was provided. Do not expose these services or change public infrastructure until those are supplied.

## Verified features

- Public pages: Tera branding, original attribution, `/features`, `/features/reservations`, `/pricing`, `/about`, image assets, desktop and 390px mobile layout.
- Guided signup wizard: step 0 → step 1 → back, no tenant created by the UI test.
- Owner registration and email-code verification (QA used dev-only fixed code via DB hash injection).
- Staff login and authenticated session.
- Table management and table activation PIN.
- Product/menu creation.
- Order placement, KOT/kitchen status progression.
- Billing: cash settlement and payment record creation.
- Reservations: create and list.
- Inventory: item create and list.
- Reports, kitchen, orders, products, tables, reservations, catalog/inventory UI routes.
- Tenant WebSocket: opened successfully through HAProxy with no 403/1008 auth errors.
- Production images: `pos-back:latest`, `pos-master-front`, `pos-ws-bridge:latest` build successfully.

## Verification evidence

- `curl http://127.0.0.1:4202/api/health` → `200`; `/`, `/features`, `/pricing` → `200`.
- Full six-service dev stack running/healthy: `pos-back`, `pos-front`, `pos-haproxy`, `pos-postgres`, `pos-redis`, `pos-ws-bridge`.
- Restart recovery: `docker compose -f docker-compose.yml -f docker-compose.dev.yml restart back front ws-bridge haproxy` → health and app both `200` after 11s.
- Core API QA (`tmp/tera-release/e2e.mjs`) on a clean bootstrapped DB: all steps passed.
- Browser QA on restored stack: owner login, eight authenticated routes, mobile 390px checks on `/dashboard`, `/features`, `/login`, no uncaught browser errors.
- WebSocket test after restart: `>>> RESULT: WebSocket connection opened successfully.`
- Backend snapshot comparison: baseline and rebranded code have the same 12 pre-existing pytest failures; rebrand introduced no new failures.
- Four upload-related tests that failed only because `/app/uploads` was read-only passed with a writable tmpfs.
- Targeted rerun of the 12 previously failing test files on a clean, properly bootstrapped DB with writable uploads: **15 passed, 2 failed**. The 2 remaining failures are `tests/test_customer_display_invoice_email.py` fixtures that require an existing tenant/tables; they fail at fixture setup (`assertIsNotNone(tenant)`), not in product code. Not release blockers.

## Production configuration

Use `config.env.production.example` as the template. Never copy the local `config.env` to production.

Required values:

- `SECRET_KEY` and `REFRESH_SECRET_KEY`: generate separately, e.g. `openssl rand -hex 32`.
- `CORS_ORIGINS`: explicit HTTPS origin(s), e.g. `https://your-domain.tld`. `*` is rejected in production.
- `API_URL=/api`, `WS_URL` empty unless a separate WS host is intended.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: strong database credentials.
- `EMAIL_FROM_NAME=Tera`.
- SMTP, Stripe, Revolut, Verifactu and marketplace values only if those features are enabled.

Production safety checks verified with a throwaway env file:

- Placeholder secrets rejected.
- Placeholder CORS and wildcard CORS rejected.
- `PRODUCTION=true`, Secure cookies enabled, `/api/docs` disabled.
- HAProxy publishes 80 and 443.
- Backend and ws-bridge share `SECRET_KEY`.

Important: Compose passes `SECRET_KEY` to both backend and ws-bridge but does **not** pass `REFRESH_SECRET_KEY`. The filled `config.env` mounted at `/app/config.env` must contain the real `REFRESH_SECRET_KEY`.

Missing for public deployment:

- TLS certificates in `certbot/haproxy-certs` (`certbot/` exists, the certificate directory does not).
- Target host, domain, DNS records and operator access.
- Explicit authorization to publish.

## Deploy procedure (target Linux host)

```bash
cd /path/to/pos-master
cp config.env.production.example config.env
# edit config.env: secrets, DB credentials, CORS_ORIGINS, SMTP/domain values
mkdir -p certbot/haproxy-certs
# place valid fullchain/privkey PEM files for HAProxy there

docker compose --env-file config.env -f docker-compose.yml -f docker-compose.prod.yml build back front ws-bridge
COMPOSE_FILES='docker-compose.yml docker-compose.prod.yml' ENV_FILE=config.env ./scripts/bootstrap-tera-db.sh
docker compose --env-file config.env -f docker-compose.yml -f docker-compose.prod.yml up -d
curl -fsS http://127.0.0.1/api/health
curl -s -o /dev/null -w '%{http_code}\n' https://your-domain.tld/
```

`scripts/bootstrap-tera-db.sh` starts DB+Redis, waits for readiness, pre-creates SQLAlchemy enum types (including inventory enums), runs `create_all()`, then applies all migrations and the idempotent sync. Without the enum pre-creation, a fresh DB fails with `type "staff_contract_kind" does not exist` or `unitofmeasure` errors.

If the target follows the existing amvara9 deployment pattern, review `scripts/deploy-amvara9.sh` and `docs/0004-deployment.md` before adapting it; it is host-specific and must not be copied unchanged.

## Demo account setup procedure

1. Start the stack and bootstrap/migrate the DB.
2. Optional seed for a fully populated demo tenant:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.seeds.seed_demo_tables
   docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.seeds.seed_demo_products
   ```
3. Open `/register` and create an owner account. In dev, set `OWNER_SIGNUP_FIXED_CODE=424242` in `config.env` before registration to use a known verification code; never use a fixed code in production.
4. Log in at `/login`, then verify `/dashboard`, `/tables`, `/orders`, `/kitchen`, `/reservations`, `/catalog-inventory`, `/reports`.
5. Do not publish demo credentials; create per-user accounts on the target system.

## Known issues and limitations

- Full backend suite is not green: 12 pre-existing failures also present in the pre-rebrand baseline. They are fixture/environment issues (seeded tenant/tables, read-only uploads, disposable schema), not rebrand regressions or critical core-flow blockers.
- The 2 invoice-email fixture failures above need existing tenant/tables; they pass product code paths when the seed data exists.
- Arabic locale is missing 35 keys; pre-existing and outside this release.
- `front/scripts/test-register-page.mjs` targets the old one-step signup form; use `test-guided-signup-wizard.mjs` instead.
- Real payment, marketplace and outbound email flows were not executed; dev SMTP is not configured.
- The local stack was recreated after a Docker engine restart wiped its containers/volumes. No user data existed in those volumes; the current DB was bootstrapped and re-verified.
- `/inventory` is module-gated and redirects to `/dashboard` for new tenants; use `/catalog-inventory`.
- After the front restart, logs showed a non-fatal esbuild `all goroutines are asleep - deadlock!` warning followed by a successful watch-mode startup; app returned `200` and browser QA passed. No TypeScript/Angular build errors.

## Rollback

- Keep a `pg_dump` of the production DB before deploying.
- Keep the previous image IDs/tags available.
- On failure: stop the stack, restore the DB dump, redeploy the previous image set, and re-run `curl /api/health` plus a browser smoke.
- Do not use `docker compose down -v` for rollback; it deletes named volumes and all database data.

## Public demo (temporary)

- Repository: https://github.com/Aaditya022/Tera
- Demo: https://donor-chart-kinds-warming.trycloudflare.com
- Demo owner: `demo@terademo.app` / `TeraDemo-2026!` (tenant 6)
- Demo dataset and three-minute recording sequence: `docs/tera-demo.md`
- The quick tunnel requires this local machine and the `tera-cloudflared` container to keep running; the URL changes if they restart.
- For public exposure, dev secrets were replaced with random values, `PRODUCTION=true` was enabled, CORS was restricted to the tunnel origin, and `/api/docs` returns 404. HAProxy health checks now use `/health`.
