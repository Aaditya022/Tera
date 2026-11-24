# Tera Public Demo

The demo is hosted through a temporary Cloudflare quick tunnel to the local stack on `localhost:4202`.

**Public URL:** https://donor-chart-kinds-warming.trycloudflare.com

**Demo owner login:** `demo@terademo.app` / `TeraDemo-2026!` (tenant 6 — intentionally public demo account, no real customer data)

The tunnel is temporary. It works only while this local machine, Docker stack and `tera-cloudflared` container remain running. Restarting the machine or container changes the URL.

## Demo dataset (tenant 6)

- Six activated tables `T01`–`T06`, each with a four-digit activation PIN.
- Eight menu items: Tera Margherita Pizza, Truffle Mushroom Pizza, Iberico Durum Bowl, Grilled Sea Bass, Patatas Bravas, Andalusian Gazpacho, Spanish Cheesecake, Tera House Lemonade.
- Four orders with different states: ready, preparing, paid, pending — enough to show kitchen tickets and billing history.
- One reservation for tomorrow at 19:30 for four guests.
- Five inventory items: mozzarella, tomatoes, flour, lemons, olive oil.

## Three-minute recording sequence

1. **0:00–0:20 — Public landing.** Open the public URL, show Tera branding, then click through `/features` and `/pricing` to prove the landing page reaches the working app.
2. **0:20–0:40 — Login.** Go to `/login`, sign in with the demo owner account, land on `/dashboard`.
3. **0:40–1:00 — Dashboard and tables.** Show dashboard KPIs, open `/tables`, point out the six active tables and activation PINs.
4. **1:00–1:20 — Menu management.** Open `/products`, show the eight sample items, then open the public menu for a table (`/menu/<table-token>`).
5. **1:20–1:50 — Order and digital KOT.** From the public menu, add two items and place an order using the table PIN. Open `/kitchen` and show the new live ticket. Advance the order through `preparing` → `ready`.
6. **1:50–2:15 — Billing.** Open `/orders`, settle the order with cash, show the payment record and paid status.
7. **2:15–2:35 — Reservations.** Open `/reservations`, show tomorrow's demo reservation and the party size/time.
8. **2:35–2:50 — Inventory.** Open `/catalog-inventory`, show the five demo ingredients.
9. **2:50–3:00 — Reports.** Open `/reports`, show that the day's orders and payments are reflected.

## Public QA results

Verified through the public HTTPS URL: registration + verification, login/session, dashboard, table management, menu management, order placement, digital KOT, kitchen display, order status updates, billing/payment record, reservations, inventory, reports, mobile layout and WebSocket connection. API docs are disabled publicly (`/api/docs` → 404).

Email delivery was not tested; verification codes for QA accounts were injected into the local DB. Real payment providers and marketplace integrations were not used.
