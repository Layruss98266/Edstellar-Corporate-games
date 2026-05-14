# Game Mechanics Reference

> The standardised infrastructure every playable Engage game should implement.
> Use **Improv Challenge** (`improv-challenge.html`) and **Egg Drop Pro** (`egg-drop.html`) as the two reference implementations.

When a new game graduates from concept to playable demo, this document is the engineering checklist. Every item that applies to your game's mechanic should ship. Items that don't apply (e.g. score dots in a non-scoring game) can be skipped — but the **bold-tagged "Required"** items below must ship for the game to qualify as a v1 playable.

---

## 1. Brand & Visual Standards · **Required**

| Token | Value | Use |
|---|---|---|
| `--deep` | `#0B3C5D` | Headings, dark gradient stops |
| `--blue` | `#2563EB` | Primary CTA |
| `--blue-dark` | `#1D4ED8` | Hover state |
| `--sky` | `#38BDF8` | Accent, progress bars |
| `--bg` | `#F5F7FA` | Page background |
| `--heading` | `#0F172A` | Body text headings |
| `--success` | `#10B981` | Round survives, positive feedback |
| `--warning` | `#F59E0B` | Mid-tier scores, gold, alerts |
| `--danger` | `#EF4444` | Round fails, destructive |
| `--gold` | `#F59E0B` | 1st place podium |

Layered radial-gradient page background, Inter font stack, system fallbacks, no web fonts.

---

## 2. Page shell · **Required**

```html
<body data-phase="setup" data-teams="0" data-rounds-played="0">
  <a class="skip-link" href="#gameArea">Skip to game</a>
  <div class="sr-only" id="ariaAnnouncer" role="status" aria-live="polite" aria-atomic="true"></div>
  <a class="back-pill" href="../game.html?id=<slug>">← Back to Engage</a>
  <div class="mode-banner" id="modeBanner"></div>
  <canvas id="confetti" aria-hidden="true"></canvas>
  <div class="shell"> ... </div>
</body>
```

- **`back-pill`** top-left links back to the Engage detail page for this game.
- **Skip link** + **ARIA announcer** ship on every page.
- **Confetti canvas** is fixed full-screen, z-index 1100, pointer-events none.
- **`body[data-phase]`** drives progressive disclosure via CSS — see section 7.

---

## 3. Hero card (compact) · **Required**

- Eyebrow pill: `Edstellar Engage · Workplace Game`
- H1: game title, max 46px on desktop
- 1-paragraph description (≤ 2 lines)
- 4 actions, **all required**: **Play Demo Now** (success), **Setup Custom Game** (primary), **How to Play** (secondary), **Reset** (tertiary)
- The **Reset** button is mandatory on every playable game — it must clear teams, rounds, log, and the `localStorage` state key, then return the UI to the setup phase. Show a `confirm()` before destroying state.
- Decorative radial blob top-right inside `.hero-card::after`

---

## 4. Game Snapshot card · **Required**

Aside next to the hero. Contains:
- **4-stat grid**: Teams · Round · (game-specific stat) · Phase
- **Coins/score strip** (dark gradient): primary game KPI + secondary pill + **streak pill** (only when ≥ 2 days)
- **Mini "core rule" card** with keyboard hints
- **Tools row**: High-contrast toggle · Shortcuts button · Autosave indicator

---

## 5. Flow stepper · **Required**

5-step horizontal pill row showing game phases. Active step gets brand-blue background.
Default phases: `Setup → Build/Prompt → Event → Action → Review`. Adapt names per game.

---

## 6. Setup panel — three numbered sections · **Required**

```
[1] Quick start (Optional)
  - "Use 3 demo teams" + "Save as template" buttons
  - Templates pill row appears below when saved

[2] Game settings (Required)
  - Language dropdown (14 entries — see section 12)
  - Game-specific selects laid out as 2×2 grid
  - Live estimator card: "~9 min · N options available"

[3] Teams (Required)
  - Tight name+Add row
  - Members textarea
  - Roster counter ("3 teams")
  - Team list with inline edit (name, members, color swatch, avatar)
```

Plus a **sticky Start Game CTA** at the bottom with backdrop-blur, smart label:
- 0 teams → disabled "▶ Start Game" + "Add at least 1 team"
- Ready → "▶ Start Game · N teams · ~X min total"
- Mid-game → "▶ Continue: Round N"
- Game complete → "↻ New game"

---

## 7. Phase-aware status strip · **Required**

Single status bar above the gameplay area. Different gradient per phase + bottom progress bar.

```css
body[data-phase="setup"]   .status { neutral blue }
body[data-phase="build"]   .status { green tint }
body[data-phase="prompt"]  .status { green tint }
body[data-phase="perform"] .status { green tint }
body[data-phase="event"]   .status { amber tint }
body[data-phase="drop"]    .status { red tint }
body[data-phase="score"]   .status { purple tint }
body[data-phase="review"]  .status { purple tint }
```

Inside: `<strong>statusTitle</strong>` + `<span>statusSub</span>` + `<div class="timer">` + bottom `.status-progress` fill.

**Timer** has color states: neutral → `warn` (amber pulse) at 30s → `danger` (red pulse) at 10s. Hidden via `body[data-phase="setup"] .timer { display:none }`.

---

## 8. Team customisation · **Required**

Each team object:

```js
{
  id, name, members: [],
  score: 0, tests: 0, rounds: 0,
  color: TEAM_COLORS[i % 8],
  avatar: TEAM_AVATARS[i % 8],  // emoji
  badges: [{id, at}]
}
```

- 8 brand-aligned color palette: `['#0B3C5D','#2563EB','#10B981','#F59E0B','#7C3AED','#EC4899','#0EA5E9','#F97316']`
- 8 avatar emojis: `['🦅','⚡','🔥','🌟','🚀','🛡','🎯','🦄']`
- Inline edit form: name input, members textarea, swatch row, avatar picker
- **Member pills** render everywhere a team is shown — with a `::before` colored dot using the team's color
- **Member count badge** (`👥 N`) next to every team name

---

## 9. Languages · **Required**

14-language dropdown with native script + English name:

```
EN · English | हिं · Hindi | ع · Arabic (RTL) | ES · Spanish |
FR · French | DE · German | PT · Portuguese | 日 · Japanese |
한 · Korean | 中 · Chinese | RU · Russian | IT · Italian |
ID · Indonesian | TR · Turkish
```

- For prompt-based games: real translated prompt packs in each language (8-10 each minimum).
- For build-based games: language affects only UI strings; materials/mechanics stay technical.
- `document.body.dir = lang === 'ar' ? 'rtl' : 'ltr'`
- Persisted in `localStorage` and synced into the share-URL state.

---

## 10. Currency / power-ups (optional, when game supports it)

Either a per-team **EngageCoins** balance (Improv) **or** a per-round **budget** (Egg Drop). Pick one model per game:

| Model | When to use | Example |
|---|---|---|
| Coins | Skill-based games where teams earn and spend across rounds | Improv (50 start, 20-80 per power-up) |
| Budget | Resource-allocation games where each round resets | Egg Drop (100 per round) |

Power-ups (if coins): 5 max, displayed as a card row that becomes visible during play.
Random events (if budget): 6-10 events that fire mid-round to change cost / difficulty / mechanics.

---

## 11. Scoring · **Required**

- **Score dots** (10-dot clickable scale) for criterion-based scoring (Improv). Color-tiered: red (1-3) / amber (4-6) / green (7-10).
- **+/- buttons + qty** for resource-based games (Egg Drop materials).
- **Live running total** chip that flashes amber on change.
- **Floating "+X" particle** animation on every score change. Green for positive, red for negative.
- **Crown** (`leader` class) on the current top team's card.
- **Quick-score presets** (e.g. 30/42/54) for fast facilitation.

---

## 12. Plot twists / random events · **Required**

10 short, varied disruptors that fire mid-round. Each:

```js
{ id, name, desc, mod: {} }  // mod can affect cost, drag, difficulty, etc.
```

Banner display: amber gradient, dismissable, logged with the round entry.

---

## 13. Leaderboard with podium · **Required**

Top 3 get **gold / silver / bronze** card backgrounds.
- Rank 1: gold gradient background, deep amber text, score 30px
- Rank 2: slate gradient, score 26px
- Rank 3: bronze gradient, score 24px

Card layout: `rank · avatar · name+members+meta · score`.

---

## 14. Tabs · **Required**

5-6 tabs in a single row:
```
[▶ Play] [🏆 Leaderboard] [📊 Analytics or Review] [🎖 Awards/Badges] [💬 Reflection] [📋 Round Log]
```

Each tab has a keyboard shortcut hint (`P / L / A / B / R`).

**Conditional visibility**: Analytics / Awards / Round Log only show after at least 1 round is played:
```css
body[data-rounds-played="0"] .tab[data-view="analytics"],
body[data-rounds-played="0"] .tab[data-view="awards"],
body[data-rounds-played="0"] .tab[data-view="log"] { display:none }
```

**Hidden-information games** add a `🛡 Judge` tab gated behind a confirm prompt — see **§34**.

---

## 15. Round summary + Final winner · **Required**

Two-tier celebration:

1. **Round summary modal** fires after every `finishRound` / `runDrop`. Header has gradient winner banner with 👑 crown + winner name + delta. Body lists all teams ranked with response excerpts or build summary. Single confetti burst.

2. **Final winner overlay** fires at end of `maxRounds` (Improv) or 3rd drop (Egg Drop). Header reads **"🏆 [Champion] wins the game"** with total stats. Body shows full ranked standings with member pills. **Double confetti burst** (immediate + 850ms later). CTA: "↻ Play again".

---

## 16. Achievement badges · **Required**

**10-badge system** per game. Each badge:
```js
{ id, icon, name, desc }
```

Two universal badges:
- 🥇 **First Win** (won round 1)
- 👑 **Champion** (won the game)

Game-specific 8 badges driven by gameplay mechanics. Examples:

| Improv | Egg Drop |
|---|---|
| 🎩 Hat-Trick (3 in a row) | 🥚 Iron Egg (survived all 3) |
| 🌟 All-Rounder (6+ each criterion) | 🍀 Lucky Roll (survived <30%) |
| 🏗 Master Builder (10 Builds) | 🛡 Strongest Build |
| 🎯 Solution Closer (10 Solution) | 🎯 Best Placement |
| 📈 Comeback Kid | 📈 Comeback Kid |
| 💰 Coin Hoarder (100+ coins) | 💰 Budget Master (<50 + survived) |
| ⚡ Lightning Round | ⚡ Quick Builder |
| 📖 Storyteller (5+ responses) | 🌟 All-Rounder (every round survived) |

Auto-awarded after `finishRound`. Toast notification on earn. Full gallery on the **Badges** tab.

---

## 17. Analytics tab (optional, when game has measurable criteria)

For Improv-style games with criterion scoring:
- **Canvas radar chart** averaging criteria across rounds
- **Canvas line chart** of round totals
- **Weakest criterion** pill
- Mini badge row of earned achievements

Both charts are pure canvas — no libraries.

---

## 18. Auto-coaching tips / auto-review · **Required**

End-of-round auto-generated coaching (Improv) or auto-generated review (Egg Drop) that:
- Identifies the weakest dimension
- Links to the relevant Edstellar training course (`https://www.edstellar.com/course/<slug>`)
- Surfaces tag patterns or build patterns ("3 blocks detected this round")
- Renders inside the round-summary modal

This is the **Edstellar reinforcement wedge** — every game must connect back to the training catalog.

---

## 19. Modes · **Required**

Three modes detected via URL params:
- Default (no param)
- `?mode=present` — big text, hide chrome, projector-friendly
- `?mode=play` — phone-friendly, hide setup/leaderboard

`body.classList.add('mode-present'|'mode-play')` drives CSS overrides.
Mode banner top-right with "exit" link.

---

## 20. Share modal · **Required**

Opens from the Reflection / Review tab. Contains:
- **Shareable URL** with full session state base64-encoded into `#s=` hash
- **Slack/Teams card text** (winner + drops + replay link)
- **iframe embed snippet** for Confluence/Notion
- **"Open Presenter View"** and **"Open Player View"** buttons

`loadFromHash()` runs on boot to restore state from `#s=` if present.

---

## 21. 14-day reinforcement reminder · **Required**

Single button in Reflection / Review: **"📅 Schedule reminder (14d)"**.
Generates a downloadable `.ics` calendar file:
```
SUMMARY: <Game name> - Reinforcement Session
DESCRIPTION: Replay with the same teams. Beat the forgetting curve.
DTSTART: now + 14 days at 10:00 AM
DURATION: 30 minutes
```

---

## 22. Exports · **Required**

- **JSON export** — full game state with teams, rounds, language, custom data
- **CSV export** — round-by-round, one row per team, Excel-ready
- **Print-friendly stylesheet** — hides buttons/setup/toasts, keeps panels

---

## 23. Undo last save · **Required**

Snapshot teams + roundLog + state **before** every `finishRound`/`runDrop` mutation.
12-second **"↶ Undo"** banner appears bottom-center after every save.
Click → restores everything, recomputes `currentRound`, closes summary, ARIA-announces.

---

## 24. Edit historical round / drop (optional but recommended)

`✎ Edit` button on every Round Log entry → inline editor with number inputs → save recomputes team totals via delta.

---

## 25. Saved session templates · **Required**

Setup config (mode, time, language, rounds, etc.) saveable as named pills.
Click a pill to reload that config. Click `×` to delete.

---

## 26. Custom content creator (optional)

For Improv: custom prompt creator with import/export JSON pack.
For Egg Drop: future custom material creator.
Always collapsible (`<details>`) inside the setup panel.

---

## 27. Accessibility · **Required**

- **Skip link** (`.skip-link`) to `#gameArea`
- **`#ariaAnnouncer`** with `aria-live="polite"` for round events
- **High-contrast mode** toggle in snapshot (`body.hc` class, persisted)
- `aria-label` on all icon-only buttons
- `aria-valuemin/max/now` on score dots (role="slider")
- `prefers-reduced-motion` respected — all animations short-circuit to ~0
- Keyboard navigation: every interactive element reachable via Tab, visible focus rings (3px brand-blue 40% alpha)

---

## 28. Keyboard shortcuts · **Required**

Universal set every playable game implements (adapt verbs to game):

| Key | Action |
|---|---|
| `Space` | Start round / pause |
| `D` | Run drop / Finish action |
| `E` | Random event |
| `N` | Next prompt / Next team |
| `T` | Plot twist (if coins-based) |
| `F` | Fullscreen |
| `P` | Play tab |
| `L` | Leaderboard tab |
| `A` | Analytics / Awards tab |
| `R` | Reflection / Review tab |
| `B` | Badges tab |
| `?` | Open cheat-sheet |
| `Esc` | Close any modal |

---

## 29. Cheat-sheet modal · **Required**

Press `?` opens a full-screen modal with 6 sections:
1. Keyboard shortcuts
2. Power-ups / Materials / Events (game-specific)
3. Coaching tags / Scoring criteria (game-specific)
4. Badges (10 entries with unlock criteria)
5. Modes
6. Accessibility features

Also reachable via the **⌨ Shortcuts** button in the snapshot tools row.

---

## 30. Auto-save · **Required**

Every state mutation calls `saveState()` which writes to `localStorage` and updates `lastSaveAt`.
**Auto-save indicator** in snapshot tools row updates every 5s: "Saved Xs/Xm/Xh ago".

Storage key naming convention: `edstellar<GameName>V<version>`.

---

## 31. Daily streak tracker · **Required**

`updateStreak()` on boot reads `edstellar<Game>LastSession` and `edstellar<Game>Streak` from localStorage. Increments on consecutive days. Streak pill (🔥 N-day streak) visible only when streak ≥ 2.

---

## 32. Game registration in the catalog · **Required**

In `engage-prototype/assets/games.json`, set:
```json
{
  "slug": "<your-slug>",
  "playable": true,
  "playUrl": "./play/<your-slug>.html",
  "walkthrough": [...4 entries...],
  "skills": [...],
  "howToPlay": [...],
  "reviewQuestions": [...3...],
  "keyTakeaway": "...",
  ...
}
```

Also extend `_build/parse_master.py`'s `PLAYABLE` dict:
```python
PLAYABLE = {
    "improv": "./play/improv-challenge.html",
    "egg-drop": "./play/egg-drop.html",
    "<your-slug>": "./play/<your-slug>.html",
}
```

Then re-run `python _build/parse_master.py` so future master-HTML edits preserve the playUrl.

---

## 33. Quality bar — definition of done

A playable game v1 ships when **all of the following are green**:

- [ ] Renders correctly from `file://` (no fetch dependencies)
- [ ] Renders correctly via the Vercel deployment at `/play/<slug>.html`
- [ ] Works in Chromium, Firefox, Safari (manual)
- [ ] Mobile breakpoint at ≤768px collapses cleanly
- [ ] Print preview hides buttons/setup but keeps panels readable
- [ ] Reduced-motion users see no animations
- [ ] All keyboard shortcuts work
- [ ] Cheat-sheet opens via `?` and lists everything game-specific
- [ ] Share URL round-trips full game state
- [ ] All 10 badges have unlock paths in the gameplay
- [ ] Final winner overlay fires correctly with double confetti
- [ ] Undo works and recomputes totals correctly
- [ ] 14 language dropdown switches at least the dropdown labels and `body.dir` (RTL on Arabic)
- [ ] Custom content (prompts/materials) can be added and survives reload
- [ ] Reset button in the hero row clears all state (teams, rounds, log, storage key) after a confirm
- [ ] If the game has hidden information, the Judge tab gates behind a confirm and auto-locks on leave (§34)

---

---

## 34. Facilitator / Judge view (optional, when game has hidden information)

Some games hide information from the rest of the room that exactly one person — the facilitator or host — must be able to verify. The lie in **Two Truths and a Lie**, the secret role in a Werewolf-style round, the hidden card in a deception game, the answer key in a quiz. When a game has this pattern, the host needs a private answer surface that's part of the same screen but kept away from players' eyes.

When your game has hidden information, add a dedicated **Judge** tab in the tabs row (§14) that:

- Sits between the shared `Statements` / equivalent tab and `Review` in the tab order
- Is **gated behind an explicit confirm**: clicking the tab triggers a modal — _"Open Judge view? This screen reveals every speaker's flagged answer. Hide your screen from other players before continuing."_ — that must be acknowledged before the answer key renders
- Shows the **answer key** for every active speaker/round (each player's flagged lie, the hidden role, the correct answer) using private-answer styling: `revealed lie` / `revealed truth` ribbons on each card and a `Private answer · do not show players` banner at the top
- **Auto-locks every time the user leaves the tab and returns** — the confirm modal re-fires. Never persist `judgeUnlocked = true` across tab switches.
- **Never** writes the answer key to the shared `#s=` share-URL state. Strip statements / flags before base64-encoding. You may set a `hasHiddenInfo: true` marker in the shared state so the receiving session knows to re-collect locally.
- Uses a distinct gradient on the tab (purple `#7C3AED` works well — visually separates it from the brand-blue active tab so the host always knows which mode they're in)

```js
function switchView(v){
  if(v === 'judge' && !judgeUnlocked){
    $('judgeGateOverlay').classList.add('show');
    return;
  }
  // ... swap tab visibility
  if(v !== 'judge') judgeUnlocked = false; // auto-lock on leave
}
function confirmJudge(yes){
  $('judgeGateOverlay').classList.remove('show');
  if(yes){ judgeUnlocked = true; switchView('judge'); }
}
```

Reference implementation: [`two-truths-and-a-lie.html`](two-truths-and-a-lie.html) — see `renderJudge()`, `confirmJudge()`, and the `#judgeGateOverlay` modal.

---

## Reference implementations

- [`improv-challenge.html`](improv-challenge.html) — prompt-based, criterion scoring, EngageCoins economy, plot twists
- [`egg-drop.html`](egg-drop.html) — build-based, drag-and-drop placement, budget-per-round, random events, drop animation
- [`two-truths-and-a-lie.html`](two-truths-and-a-lie.html) — hidden-information game with Judge view, voter queue, coin-based power-ups, plot twists, private statement editor

Read those files end-to-end before starting a new game. Every infrastructure pattern in this document has a working example in one or more of them.
