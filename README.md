# Edstellar Corporate Games

Concept work and an interactive prototype for **Edstellar Engage** — a proposed corporate engagement and learning-reinforcement platform built around Edstellar's training catalog.

## Contents

- **`engage-prototype/`** — static prototype (10 marketing pages + 1 playable game). Vanilla HTML/CSS/JS, no build step. See [`engage-prototype/README.md`](engage-prototype/README.md).
- **Strategy & research** — `Edstellar_Engage_Concept_Document.docx`, `Edstellar_Engage_Games_Research.docx`, `Edstellar_Blogs_Games_Catalog.docx`, `Edstellar_Engage_Game_Page_Concept.docx`.
- **Game content** — `Edstellar_Engage_All_Games_Master.html` (215 structured game cards across 14 blog sections) and `Edstellar_Engage_Individual_Game_HTML_Files/` (216 standalone modules).

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
