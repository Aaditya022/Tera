# Tera rebrand: scope, change log, and verification

## Plan and reference classification

This is a display-branding change to Satisfecho POS, not a new implementation.
Original authorship, Amvara Consulting S.L. attribution, contributor credits,
AGPL notices, LICENSE, and third-party acknowledgements remain applicable.

1. Inspect branding and establish a build/test baseline.
2. Change reviewed display text, keeping translation keys and contracts stable.
3. Replace product marks with original geometric Tera artwork.
4. Build Angular, run backend tests against an isolated database, and smoke-test
   the available local application and workflows.
5. Record changed files, actual results, and deployment limitations here.

| Reference family | Classification | Action |
| --- | --- | --- |
| Product names in navigation, titles, metadata, translation values, manuals | Safe display copy | Tera |
| Registration email copy, default sender display name, wallet fallback names | Safe display copy | Tera; configured sender names remain authoritative |
| Delivery labels in printing and WebSocket presentation fields | Safe display copy | Tera Delivery; channel enum and message structure unchanged |
| Product SVG/PNG/ICO marks, share image, README banner | Safe product assets | Original T monogram; retain environment-specific icon colours |
| `satisfecho_delivery`, delivery API paths, feature slugs, schema names, translation keys | Internal/public contracts | Preserve |
| Database models, migrations, auth issuer, wallet IDs, TSE record identifiers | Compatibility-sensitive | Preserve |
| URLs, email addresses, support login identity, domains, certificate paths, package names | External identity/configuration | Preserve; no invented Tera endpoints |
| Upstream support-access copy | Actual upstream support identity | Preserve alongside the existing upstream support email |
| Terms/privacy bodies and upstream company statements | Legal/operator attribution | Preserve; do not relabel upstream legal promises as Tera promises |
| LICENSE, copyright, credits, historical changelog, archived tasks/reviews | Legal/historical record | Preserve |
| Tenant names, logos, restaurant microsites, uploaded assets | Customer-owned branding | Preserve |
| Compose services/ports/volumes, environment variable names | Deployment contracts | Preserve; only default mail display name is eligible |

## Baseline (before branding edits)

- This download contains no `.git` directory. Branch synchronization and history
  comparison are unavailable. No Git repository is initialized; no commit/push.
- Docker and existing frontend/backend images are available. PostgreSQL and Redis
  are healthy; application containers were created but not running.
- Angular production browser + server build: passed. Existing warnings: four
  NG8107 optional-chain warnings in the menu, menu stylesheet budget, and
  CommonJS `dijkstrajs`/`pngjs` dependencies.
- Initial backend pytest invocation without database networking: failed to connect
  to localhost:5432, then timed out at 120 seconds. A fail-fast rerun confirmed
  the missing PostgreSQL connection (1 passed, 1 failed). This is not a passing
  baseline; rerun against an isolated test database before attributing failures.

## Verification strategy

- Use existing container dependencies; no host installations.
- Compare the resulting source changes with a local pre-change snapshot, excluding
  secrets, customer assets, and generated build output.
- Verify locale keys and interpolation tokens remain unchanged; inspect remaining
  legacy names against the classification above.
- Run production Angular compilation, backend pytest, Compose configuration
  validation, service/log checks, and local HTTP/browser smoke tests.
- Cover login/registration, dashboard, tables, reservations, orders, kitchen,
  billing, inventory, and WebSockets with existing tests wherever possible.
- Do not send real mail, charge payment providers, or mutate customer data for
  verification. Use isolated test data; report unavailable end-to-end checks.

## Change log

Display-only rebrand to Tera. Internal names stay unchanged: `satisfecho_delivery`,
routes, API paths, translation keys, env var names, compose services/ports, migrations,
models, database schema, `LICENSE`, and legal text. The Satisfecho/Amvara attribution
remains visible and is reworded rather than removed.

### Changed

- Locale display copy (10 locales): `LANDING.BRAND_NAME`, About/delivery/feature copy,
  `DOC_TITLE`, company attribution (`COMPANY_OPERATOR`/`COMPANY_TITLE`).
- Frontend: metadata/SEO, landing hero and brand mark, feature landings and detail,
  customer home, paywall, sidebar brand, favicon versioning.
- Backend display strings: email from name, user messages, loyalty wallet fallbacks,
  delivery/print labels, API title; matching delivery-order test expectation.
- Docs/manuals/README headings, i18n seed script.
- Original Tera SVG assets (`front/public`, `back`, `docs`) plus generated
  `favicon.png`, `favicon.ico`, `og-image.png`; generator with self-checks in
  `scripts/generate-tera-assets.py`.
- Base compose only: `EMAIL_FROM_NAME` default.

### Verification

- Snapshot check: PASS. 54 files changed; locale keys/placeholders/links unchanged;
  backend AST, models, Angular routes, API service, dev/prod compose, and `LICENSE`
  unchanged.
- Angular production build: passes; only pre-existing warnings (NG8107, stylesheet
  budget, CommonJS deps).
- Compose config validation: dev and prod overlays pass.
- Browser smoke (disposable DB, host Chrome via CDP bridge): landing title/metadata/
  attribution and seven image endpoints; registration + verification; staff login;
  authenticated dashboard, tables, reservations, staff orders, kitchen,
  catalog-inventory, reports; desktop/mobile brand links; no page errors. Guided
  signup wizard step 0 → 1 → Back passes.
- WebSocket: authenticated tenant connection succeeds after recreating `ws-bridge`
  with the current `SECRET_KEY`. The earlier 1008 was a stale-container env mismatch,
  not a code change.
- Backend pytest baseline vs after: identical 12 pre-existing failures in both runs
  (inventory lock timeouts, missing `product_recipe` in the disposable DB, invoice
  email expectations). Four extra upload-test failures in the after run were caused
  by the read-only `/app/uploads` bind; all four pass when rerun with a writable
  uploads tmpfs (`4 passed`). No rebrand-related regression observed.

### Limitations

- Full suite is not green on a fresh disposable DB (pre-existing test isolation and
  enum bootstrap issues).
- No real payment, marketplace, or email delivery flows executed.
- Arabic locale still misses 35 keys; this predates the rebrand.
