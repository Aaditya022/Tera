# Tera branding audit

Audit date: **2026-11-24**. Scope: every tracked file in the public
[Aaditya022/Tera](https://github.com/Aaditya022/Tera) repository. Goal: present
Tera consistently without erasing the AGPL attribution, rewriting history, or
breaking the running demo.

The machine-readable ledger is
[`tera-branding-inventory.tsv`](tera-branding-inventory.tsv) (one row per match:
file, line, column, match, category, decision, reason). The ledger is the source
of record; the throwaway script that produced it is not part of the product.

## Method

- Scanned `git ls-files` (1,297 files) case-insensitively for `Satisfecho`,
  `Gustazo`, and the standalone token `POS2`; image bytes and filenames were
  checked separately.
- Classified every match as **Attribution**, **Historical documentation**,
  **Internal technical identifiers**, or **Product branding**, then decided
  **preserve**, **correct**, or **defer**.
- Found 1,109 literal `Satisfecho` occurrences in the last pre-audit commit
  (`73a9bce`); 1,018 remain after this pass (a net reduction of 91, even after
  adding new attribution text).
- Current ledger: **1,099 matches** — 233 historical, 133 attribution, 496
  internal identifiers, 237 product branding. 862 are preserved and 237 are
  deferred with a documented reason.
- Unpublished trees were measured but not staged: `.github/` (8 matches) and
  `agents2/` (3,229 matches in 323 files).

**Hard constraint followed:** no backend, frontend, WebSocket, Compose, or
container changes. The demo runs from bind-mounted code with hot reload; editing
it could rebuild or restart the live stack and invalidate the running URL.
Runtime copy is therefore deferred, not silently renamed.

## Corrected

Public-facing documentation now says Tera, with a working attribution section:

- `README.md`: Tera title/badges/demo link, Tera clone instructions, Tera issue
  link, star history, dedicated **Attribution** section; CORS example is
  `your-domain.tld` instead of the upstream host.
- `ROADMAP.md`: Tera product status, "Tera Delivery", Tera issue link alongside
  upstream roadmap links; numbered upstream issue links are explained and kept.
- `docs/README.md`, `docs/manual-usuario/index.html`, `docs/screenshots/README.md`:
  Tera naming, current demo screenshots, historical-screenshot labels.
- `docs/0004-deployment.md`, `docs/0011-table-reservation-user-guide.md`,
  `docs/0014-provider-portal.md`, `docs/0020-rate-limiting-production.md`,
  `docs/0030-reservation-confirmation-email-troubleshooting.md`,
  `docs/0032-github-issues-roadmap.md`, `docs/0033-postgres-adhoc-sql-table-names.md`,
  `docs/0052-saas-signup-paywall.md`, `docs/0055-public-seo.md`,
  `docs/0056-gmail-setup.md`, `docs/0059-platform-operator-portal.md`,
  `docs/0062-pos-migration-import.md`, `docs/0065-verifactu-production.md`,
  `docs/0066-club-loyalty.md`, `docs/0070-hardware-printing.md`,
  `docs/0072-tse-fiscal-compliance.md`, `docs/0073-google-analytics.md`,
  `docs/0074-fiscal-certified-middleware.md`,
  `docs/0075-promo-videos.md`,
  `docs/0080-stripe-crypto-stablecoin-payments.md`,
  `docs/0088-owner-signup-email-verify-inactive-tenants.md`,
  `docs/REVOLUT.md`, `docs/testing.md`, `docs/SECURITY-REVIEW.md`,
  `config.env.example`: product descriptions, placeholders, examples, and support
  text now use Tera or neutral `your-domain.tld`.
- Upstream host runbooks (`docs/0001-ci-cd-amvara9.md`,
  `docs/0026-haproxy-ssl-amvara9.md`,
  `docs/0027-amvara9-menu-images-troubleshooting.md`,
  `docs/0029-deployment-images-plan-next-month.md`,
  `docs/0057-deploy-css-fix-amvara9.md`, `docs/agent-loop.md`): gained an explicit
  banner that hosts, domains, and automation belong to the original project and
  are not Tera's deployment.
- Gmail setup now suggests the app name `Tera`; no functional keys, endpoints,
  enum values, or migration names were renamed.

## Preserved (and why)

| Preserved item | Reason |
|----------------|--------|
| `LICENSE`, copyright notices, contributor credits | AGPL-3.0 requires preserving notices; the README attribution links the upstream source, website, release history, and rebrand log. |
| `CHANGELOG.md` (111 matches) | Historical release record. Rewriting it would falsify what actually shipped and when. |
| Upstream issue/source links and roadmap evidence | Issue numbers refer to the original tracker. Redirecting them would make historical claims unverifiable; they are labelled as upstream. |
| `OrderChannel.satisfecho_delivery` and `order_channel=satisfecho_delivery` | Persisted enum value and database rows. Renaming without a coordinated migration breaks existing orders and reports. |
| `/public/tenants/{id}/satisfecho-delivery`, `/orders/satisfecho-delivery` | Public API contract used by the running frontend, courier, and tests. |
| `PUBLIC_SATISFECHO_DELIVERY_SESSION_ID`, `SATISFECHO_*` env keys, TSE stub token `SatisfechoTSEStub1` | Configuration/compatibility and provider handshake identifiers; not guest-visible branding. |
| File and test names (`20260720220000_order_satisfecho_delivery.sql`, `test_public_satisfecho_delivery.py`, etc.) | Referenced by migrations, imports, and test discovery; renaming adds risk without user-visible benefit. |
| `Gustazo` seed/tenant fixture data | Historical demo/sample data used by tests; it is data, not Tera's brand. |
| `pos2` network, report filenames, and compatibility paths | Infrastructure identifiers outside the product UI; changing them can break running containers, scripts, and exports. |
| `front/public/i18n/*` operator/open-source strings | They acknowledge the upstream operator and open-source foundation; changing them would misstate authorship. |
| Marketing site host/tenant mappings (`front/sites/**`, `config/marketing-sites.json`) | They point at separate upstream restaurant sites; repointing them at Tera could show the wrong content or expose demo data. |

Remaining matches in historical docs and upstream runbooks are retained as
records, now clearly labelled. `docs/screenshots/README.md` explicitly marks
retained upstream screenshots instead of presenting them as current Tera UI.

## Deferred (after submission)

These are user-visible branding, but they live in bind-mounted runtime code or
need coordinated consumer changes and a planned restart. They are not changed in
this pass:

- Static SEO shell: `front/src/index.html` meta/canonical/OG tags,
  `front/public/robots.txt`, `front/public/sitemap.xml`, `seo.service.ts`.
- Runtime copy/defaults: email sender `noreply@satisfecho.de`, email bodies,
  backend display strings and validation messages, frontend help/support
  links, legal/TOS/privacy strings in `front/public/i18n/*`.
- Marketing sites under `front/sites/**` and their canonical/tenant mappings.
- `tables.png` could not be recaptured (stayed in the loading state); it and the
  provider, courier, and platform images remain historical upstream captures.
- `.github/` CI workflow remains unpublished because the current OAuth token
  lacks `workflow` scope; `agents2/` remains local-only.

Each deferred item needs a frontend/backend rebuild plus its matching tests, and
the tunnel URL must be re-verified afterwards. Doing that during the submission
window risks the live demo for no demo-visible benefit.

## Screenshots

Captured from the running HTTPS demo on 2026-11-24 at 1440 × 1000 with demo
tenant 6: `tera-landing.png` (new), `orders.png`, `kitchen.png`, `reports.png`,
`reservations.png`, `menu.png`, `delivery.png`, `waitlist.png`. These reflect the
current Tera UI. No screenshot was edited to hide real empty states or missing
demo photos.

## Verification

- `https://donor-chart-kinds-warming.trycloudflare.com/` and `/api/health`
  returned **200** after the documentation and screenshot changes.
- Only docs, `README.md`, `ROADMAP.md`, `config.env.example`, and screenshots
  differ from the running release; no runtime file or container was touched.
- The public demo credentials and URL are intentionally documented in
  [`tera-demo.md`](tera-demo.md) and [`tera-release.md`](tera-release.md).
