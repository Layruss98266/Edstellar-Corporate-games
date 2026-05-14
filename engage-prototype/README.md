# Edstellar Engage — Prototype

Static prototype of the planned `engage.edstellar.com` product surface. Vanilla HTML/CSS/JS, no build step.

## Files

```
engage-prototype/
├── index.html              # Landing
├── games.html              # Library (215 games, filters, pagination)
├── game.html               # Game detail (?id=<slug>)
├── pricing.html            # Plans + comparison
├── use-cases.html          # HR / L&D / Managers / Enterprise
├── how-it-works.html       # Anatomy + flows + integrations
├── facilitated.html        # Facilitated session tiers
├── compare.html            # Engage vs Kahoot / Mentimeter / Gametize
├── case-studies.html       # Three stories with before/after
├── about.html              # Company, mission, roadmap
├── play/
│   ├── improv-challenge.html  # Fully playable game (14 languages)
│   └── egg-drop.html          # Fully playable build-and-drop game (14 languages)
├── assets/                 # styles.css, app.js, motion.js, games-data.js, games.json
└── _build/                 # parse_master.py + build_pages.py (re-generators)
```

## Run

Double-click `index.html`. Works from `file://` because data loads via a script tag, not `fetch`.

For HTTP: `python -m http.server 8080` → `http://localhost:8080/engage-prototype/`.

## Regenerate

```bash
# Refresh games dataset from master HTML
python _build/parse_master.py

# Re-emit the 7 marketing pages with consistent nav/footer
python _build/build_pages.py
```

## Playable games

Two fully playable workplace games. Both ship the same infrastructure layer (14 languages, presenter/player modes, share modal, .ics reminder, cheat-sheet, high-contrast, ARIA announcements, undo, autosave, badges, podium leaderboard, confetti).

**`play/improv-challenge.html`** - Improv Challenge v4
28 EN prompts + 13 language packs. Configurable rounds (3-10). EngageCoins + 5 power-ups + 10 plot twists. Auto coaching tips linked to Edstellar courses. 10 badges. Per-team radar + trend analytics. Custom prompt creator.

**`play/egg-drop.html`** - Egg Drop Challenge Pro
10 build materials × 6 random events × 3 escalating drop heights (Desk - Balcony - Building). Drag-and-drop build zone with placement scoring. Auto-generated review per drop. 10 badges (Iron Egg, Lucky Roll, Comeback Kid, Champion, etc.).

Both: client-side only, state persists in `localStorage`, opens from `file://`.

### Building the next playable game

See [`play/GAME_MECHANICS_REFERENCE.md`](play/GAME_MECHANICS_REFERENCE.md) — the standardised infrastructure every playable game should implement (33 sections, marked Required vs Optional). Use `improv-challenge.html` and `egg-drop.html` as the two reference implementations.

## Theming

All design tokens live as CSS variables at the top of `assets/styles.css`:

```css
:root{
  --brand-primary:#0B3C5D;   /* Edstellar deep blue */
  --brand-accent:#2563EB;    /* Edstellar CTA blue */
  --brand-sky:#38BDF8;
  ...
}
```

## Login-gated currency

On the public game-detail page (`game.html`), the EngageCoins panel is **read-only** — concept, starting balance, earn rules, and shop items with a 🔒 indicator. The interactive shop lives behind sign-in inside a real game session (not built in the prototype, by design). The Improv Challenge demonstrates the full mechanic in a playable form.
