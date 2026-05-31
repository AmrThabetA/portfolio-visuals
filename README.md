# Healthcare Analytics — Visual Suite

Publication-grade, interactive data visualisations for a UAE/MENA healthcare
analytics portfolio. Rebuilds key charts from the claims-denial and
chronic-disease cost projects in an editorial style modelled on
**The Athletic**, **Opta**, and **ESPN** sports-analytics graphics.

Built with **Observable Plot** (by the D3 team) — runs natively in the browser.

Author: **Amr Thabet** — Healthcare Data & Business Analyst, Abu Dhabi

---

## Why Observable Plot

The original analysis was built in Python and Tableau. This repo upgrades the
visual layer to **Observable Plot** — a JavaScript library by the D3 team that
produces D3-quality output without D3's complexity. Compared with notebook-bound
charting it gives:

- **Editorial quality** — the graded heatmap tables, annotated trend lines, and
  beeswarm distributions match professional data-journalism output
- **Web-native** — a single self-contained HTML page, no build step, no server
- **Interactive-ready** — lives directly in the browser, drops straight into a
  web app or portfolio site
- **Light + dark themes** — one toggle switches between Athletic-white editorial
  and Opta-navy dark mode

---

## Tech stack

| Tool | Role |
|------|------|
| **Observable Plot** | Charting engine (D3 team) |
| **D3** | Colour scales + number formatting |
| **Python / pandas** | Data aggregation → JSON bundle |

---

## Visual identity

A single **Tableau sequential blue** palette is applied across every chart,
graded so the **darkest shade always represents the highest value**. A secondary
amber scale highlights total/summary columns.

```
Lightest #C6DDED → Mid #5B9DC0 → Darkest #1A4A6B
Denied #A94438 · Amber #D7A800 · Green #4A9B6F
```

---

## Charts (single page, 5 charts)

| # | Chart | Style reference | Source |
|---|-------|-----------------|--------|
| 1 | Denial rate by specialty × claim type | Athletic graded goals table | P1 claims |
| 2 | Monthly denial rate trend | Athletic annotated take-on line | P1 claims |
| 3 | Claim denial vs claim size (non-finding) | Athletic beeswarm + box | P1 claims |
| 4 | Revenue leakage by denial reason | Athletic graded bar | P2 RCM |
| 5 | Avg cost by condition × emirate | Athletic graded table | P3 cohort |

---

## Project structure

```
portfolio-visuals/
├── data/
│   ├── claims_clean.csv              P1 claims dataset
│   └── chronic_disease_cohort.csv    P3 chronic-disease cohort
├── src/
│   ├── visual_suite.html             the single-page suite (open this)
│   ├── prepare_data.py               builds data.js from the CSVs
│   ├── data.js                       generated data bundle
│   └── vendor/                       offline copies of d3 + plot
└── README.md
```

---

## Running it

The page loads D3 and Observable Plot from a CDN, so with internet you can just
open it:

```bash
# open the suite directly
open src/visual_suite.html      # macOS
```

To regenerate the data bundle after changing the CSVs:

```bash
pip install pandas numpy
cd src
python prepare_data.py
```

### Offline use

If you have no internet, edit the two `<script src=...>` lines at the top of
`visual_suite.html` to point at the local vendored copies instead:

```html
<script src="vendor/d3.min.js"></script>
<script src="vendor/plot.umd.min.js"></script>
```

---

## Deploying to the web

Because the suite is a single static HTML page, it deploys anywhere:

- **GitHub Pages** — push the repo, enable Pages, point at `src/visual_suite.html`
- **Netlify / Vercel** — drag-and-drop the folder

This same Observable Plot layer becomes the dashboard inside the EHR system
(next project), so nothing here is throwaway.

---

## Data note

Datasets are synthetic, modelled on UAE/GCC health-insurance operations
(Daman/HAAD, ADNIC, AXA Gulf, BUPA Global, Cigna, MetLife, Sukoon). Figures
align with the source claims-denial and chronic-disease cost-modelling
projects. No real patient or payer data is used.
