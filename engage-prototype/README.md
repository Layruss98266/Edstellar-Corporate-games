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
│   └── improv-challenge.html  # Fully playable game (14 languages)
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

## Playable game

`play/improv-challenge.html` is a fully playable workplace-improv game.

- **14 languages** (EN + 13 packs)
- Configurable rounds (3–10), team customisation, EngageCoins economy with 5 power-ups, 10 plot twists, live coaching toolbar, auto coaching tips with linked Edstellar courses, 10 achievement badges, per-team canvas analytics (radar + trend), round summary with confetti, final-game champion overlay.
- Undo last save, edit historical round scores, auto-save indicator, cheat-sheet (`?`), high-contrast mode, ARIA-live announcements.
- Presenter mode (`?mode=present`), Player mode (`?mode=play`), share URL, Slack/Teams card, iframe embed, 14-day .ics reminder.
- Custom prompt creator with JSON pack import/export, saved session templates.
- All client-side, state persists in `localStorage`.

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
