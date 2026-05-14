# Edstellar Corporate Games

Concept work and an interactive prototype for **Edstellar Engage** — a proposed corporate engagement and learning-reinforcement platform built around Edstellar's training catalog.

## Contents

- **`engage-prototype/`** — static prototype (10 marketing pages + 3 playable games). Vanilla HTML/CSS/JS, no build step. See [`engage-prototype/README.md`](engage-prototype/README.md).
- **`Edstellar_Engage_All_Games_Master.html`** — source-of-truth for the 215 structured game cards (parsed by `engage-prototype/_build/parse_master.py` into the catalog).
- **`MIGRATION_PLAN.md`** — reference plan for the Next.js + Supabase production migration.

## Run the prototype

```bash
# Open directly:
double-click engage-prototype/index.html

# Or via local server:
python -m http.server 8080
# visit http://localhost:8080/engage-prototype/
```

## Deployment

Live on Vercel. `vercel.json` rewrites the prototype paths to the root.

## License

Internal Edstellar concept work.
