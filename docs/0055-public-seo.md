# Tera Public SEO

Short note for marketing / public surfaces of the Angular SPA (`front/`).

The document title, descriptions and local share image are branded Tera. Legacy
absolute URLs in the static shell, sitemap, robots file and server-side SEO
fallback still point to the upstream website. Correct those together after
submission using the permanent deployment origin; do not bake a temporary tunnel
URL into crawler metadata. See [the branding audit](tera-branding-audit.md).

## What we ship

| Asset / behaviour | Location |
|-------------------|----------|
| Default document title, meta description, Open Graph / Twitter tags, canonical | `front/src/index.html` (static shell) |
| Per-route titles, descriptions, robots, canonical, OG updates | `front/src/app/services/seo.service.ts` (started from `App`) |
| Share image (1200×630) | `front/public/og-image.png` |
| Crawler rules | `front/public/robots.txt` |
| Marketing URL list | `front/public/sitemap.xml` |
| Prod nginx: serve robots/sitemap as real files (no SPA fallback) | `front/nginx.conf` |

English meta copy is intentional for crawlers; guest flows (`/book/:id`, `/delivery/:id`, etc.) still set their own document titles in-component.

Staff and auth shells get `noindex,nofollow` via the SEO service (and matching `Disallow` lines in `robots.txt`).

## Verify

After deploy (or locally with the front container):

```bash
curl -sI http://127.0.0.1:4202/robots.txt   # text/plain, not text/html
curl -sI http://127.0.0.1:4202/sitemap.xml  # application/xml or text/xml
curl -s http://127.0.0.1:4202/ | head -n 40 # title + meta description present
```

Run Chrome DevTools → Lighthouse → SEO (or PageSpeed Insights) on your deployed Tera origin and `/features`. Check the canonical and share-image URLs as well as the meta-description and robots.txt audits; the legacy absolute URLs above are still pending correction.

Related issue: [#307](https://github.com/satisfecho/pos/issues/307).
