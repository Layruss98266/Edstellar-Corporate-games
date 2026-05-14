# Edstellar Corporate Games

End-to-end concept work for **Edstellar Engage** - a proposed corporate engagement and learning-reinforcement platform that turns Edstellar's training catalog into game-based experiences.

## What's in this repo

### 📄 Strategy & Research (`.docx`)

| File | What it is |
|---|---|
| `Edstellar_Engage_Concept_Document.docx` | Core product concept: positioning, pricing, GTM, KPIs, pilot plan, login-gated currency model. |
| `Edstellar_Engage_Games_Research.docx` | Competitor matrix, market sizing, cross-cut analysis, forgetting-curve data, library plan. |
| `Edstellar_Blogs_Games_Catalog.docx` | Pure catalog of all 14 source blogs and ~215 games (clean reference, no analysis). |
| `Edstellar_Engage_Game_Page_Concept.docx` | Design spec for the three core game pages (Landing, Library, Detail) + Help, Walkthrough, Currency. |

### 🎮 Game content

| File / Folder | What it is |
|---|---|
| `Edstellar_Engage_All_Games_Master.html` | One master HTML containing all 215 structured game cards across 14 blog sections. Source of truth for the prototype's data. |
| `Edstellar_Engage_All_Games_Master_Document.docx` | DOCX export of the same master. |
| `Edstellar_Engage_Individual_Game_HTML_Files/` | 216 standalone HTML modules - one self-contained page per game. |

### 💻 Interactive prototype (`engage-prototype/`)

Static HTML/CSS/JS prototype of the planned `engage.edstellar.com` product surface. **10 pages + 1 playable game:**

| Page | URL | What it covers |
|---|---|---|
| Landing | `index.html` | Hero, problem stats, value props, 14 category tiles, anatomy timeline, featured games, explore-strip, single testimonial. |
| Game Library | `games.html` | 215 games, sidebar filters with live counts, pagination (12/page), spotlight card, `/` search shortcut. |
| Game Detail | `game.html?id=<slug>` | 2-pane layout with TOC, structured fields, EngageCoins concept panel, auto-launching 4-step walkthrough. |
| Pricing | `pricing.html` | 4 plans · plan-comparison table · pricing FAQ. |
| Use Cases | `use-cases.html` | HR / L&D / Managers / Enterprise persona deep-dives. |
| How it works | `how-it-works.html` | Anatomy timeline + admin/employee flows + mechanics + integrations table. |
| Facilitated | `facilitated.html` | Session tiers ($1.5K - $15K) + regional coverage + FAQ. |
| Compare | `compare.html` | Engage vs Kahoot / Mentimeter / Gametize. |
| Case Studies | `case-studies.html` | Three long-form case studies with before/after metrics. |
| About | `about.html` | Mission, numbers, roadmap. |
| **Improv Challenge v4 (playable)** | `play/improv-challenge.html` | Fully playable in-browser game, 3,350-line single file. **14 language packs**: EN (28 prompts) + Hindi, Arabic, Spanish, French, German, Portuguese, Japanese, Korean, Chinese, Russian, Italian, Indonesian, Turkish. Every prompt: difficulty + skill tags + strong/weak examples. **Configurable rounds (3-10)** with final-winner celebration + double confetti. **Custom prompt creator** + JSON pack import/export. **Saved templates**. **Customisable teams** (name/members/color/avatar). **Live coaching toolbar** with 8 tags that auto-nudge scores + **auto coaching tips** linked to Edstellar courses. **10 badges**. **Per-team canvas analytics** (radar + trend + weakest callout). EngageCoins + 5 power-ups + 10 plot twists. **Daily streak tracker**. **Share modal** (URL + Slack card + iframe). **Presenter + Player modes**. **14-day .ics reminder**. **Undo last save** banner. **Edit historical round** scores. **Auto-save indicator**. **Cheat-sheet modal** (press `?`). **Accessibility**: skip link, ARIA-live announcements, high-contrast toggle, reduced-motion. localStorage persistence. |

#### Run it

Double-click `engage-prototype/index.html`. No build step, no server needed.

#### Regenerate data

```bash
# Refresh games dataset from the master HTML
python engage-prototype/_build/parse_master.py

# Re-emit the 7 marketing pages with consistent nav/footer
python engage-prototype/_build/build_pages.py
```

## Key product decisions captured here

- **Positioning**: Engagement, reinforcement, and culture - not "another quiz tool".
- **Wedge**: Bundled with Edstellar's existing training catalog. Reinforcement games trigger 14 and 30 days post-training.
- **Library**: 215 named games across 14 categories, parsed from existing Edstellar blog content (~200 games already documented in public posts).
- **Currency model**: **EngageCoins** - virtual in-game budget. Public pages show the **concept** (read-only). The interactive shop is gated behind login inside a live game session.
- **Pricing**: $3 → $2 → $1.25 per-employee per-month tiers + facilitated event packages from $1,500. Existing Edstellar training clients get Engage as a 15-20% contract add-on.
- **Differentiation**: 200+ game library, post-training reinforcement bundle, Edstellar facilitator network, strong India / MEA / APAC delivery, in-game currency mechanic - none of which Kahoot, Mentimeter, or Gametize offer together.

## Status

Concept and design phase. Strategy documents reviewed, prototype demo-ready for pilot-account walkthroughs. Engineering not started.

## License

Internal Edstellar concept work. All rights reserved.
