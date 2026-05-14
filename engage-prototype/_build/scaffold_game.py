"""
Scaffold a new playable Engage game wired to the shared shell.

Usage:
  python engage-prototype/_build/scaffold_game.py <slug> "<Game Title>" [--phases setup,prompt,event,score,review] [--register]

What it does:
  1. Writes engage-prototype/play/<slug>.html with:
     - <link rel="stylesheet" href="_shared/shell.css">
     - <script src="_shared/shell.js"></script>
     - Full Required infrastructure (hero, snapshot, flow, status, tabs,
       setup panel, leaderboard, awards, review, log, share, undo, cheat-sheet,
       summary overlay, judge gate placeholder, modals, autosave indicator,
       streak pill, reset button) - all already wired to Shell utilities
     - Game-specific TODOs marked with `// TODO:` comments so you know what
       to fill in: badges, plot twists / events, power-ups, scoring rules,
       round flow, reveal rules
  2. Optionally appends the slug to PLAYABLE in parse_master.py and
     regenerates games.json / games-data.js (pass --register).

This compresses new-game scaffolding from ~1700 lines of inline HTML/CSS/JS
to ~400 lines of pure gameplay logic on top of the shared shell.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PLAY_DIR = ROOT / "engage-prototype" / "play"
PARSE_MASTER = HERE / "parse_master.py"


def slug_to_storage(slug: str) -> str:
    """foo-bar-baz -> edstellarFooBarBazV1"""
    parts = re.split(r"[-_\s]+", slug.strip().lower())
    return "edstellar" + "".join(p.capitalize() for p in parts if p) + "V1"


def slug_to_const(slug: str) -> str:
    """foo-bar -> FooBar"""
    parts = re.split(r"[-_\s]+", slug.strip().lower())
    return "".join(p.capitalize() for p in parts if p)


def render_html(slug: str, title: str, phases: list[str]) -> str:
    storage = slug_to_storage(slug)
    const = slug_to_const(slug)
    flow_steps = "\n  ".join(
        f'<div class="flow-step{" active" if i == 0 else ""}" id="flow-{p}">{i+1}. {p.title()}</div>'
        for i, p in enumerate(phases)
    )
    phases_js = ",".join(f"'{p}'" for p in phases)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} - Edstellar Engage</title>
<link rel="stylesheet" href="_shared/shell.css" />
<style>
/* Game-specific styling only. Shared infrastructure is in _shared/shell.css. */
/* TODO: add phase-specific status gradients, game-layout columns, gameplay surfaces */
body[data-phase="prompt"] .status,body[data-phase="event"] .status{{background:linear-gradient(135deg,#0B3C5D,#16A34A)}}
body[data-phase="score"] .status,body[data-phase="review"] .status{{background:linear-gradient(135deg,#0B3C5D,#7C3AED)}}
.game-layout{{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:18px;margin-top:6px}}
@media (max-width:1020px){{.game-layout{{grid-template-columns:1fr}}}}
</style>
</head>
<body data-phase="setup" data-teams="0" data-rounds-played="0">
<a class="skip-link" href="#gameArea">Skip to game</a>
<div class="sr-only" id="ariaAnnouncer" role="status" aria-live="polite" aria-atomic="true"></div>
<a class="back-pill" href="../game.html?id={slug}">← Back to Engage</a>
<div class="mode-banner" id="modeBanner"></div>

<div class="shell">

<section class="hero">
  <div class="hero-card card">
    <div class="eyebrow">Edstellar Engage · Workplace Game</div>
    <h1>{title}</h1>
    <p class="hero-text">TODO: 1-paragraph game description (≤ 2 lines). What does the player do? What skill does it build?</p>
    <div class="actions">
      <button class="btn success" id="demoBtn">▶ Play Demo Now</button>
      <button class="btn" id="setupBtn">⚙ Setup Custom Game</button>
      <button class="btn secondary" id="howBtn">📖 How to Play</button>
      <button class="btn tertiary" id="resetBtn" title="Reset all game state">↺ Reset</button>
    </div>
  </div>
  <aside class="score-card card">
    <h2>Game Snapshot</h2>
    <div class="stat-grid">
      <div class="stat-box"><span class="stat-label">Teams</span><span class="stat-value" id="teamCount">0</span></div>
      <div class="stat-box"><span class="stat-label">Round</span><span class="stat-value" id="roundCount">0 / 0</span></div>
      <div class="stat-box"><span class="stat-label">TODO stat</span><span class="stat-value" id="customStat">—</span></div>
      <div class="stat-box"><span class="stat-label">Phase</span><span class="stat-value" id="phaseStat" style="font-size:18px">Setup</span></div>
    </div>
    <div class="coins-strip">
      <div>
        <small style="color:#cbd5e1;text-transform:uppercase;letter-spacing:.06em;font-size:10px;font-weight:800">Leader</small>
        <div style="font-size:18px;font-weight:900;color:#fff;line-height:1.2" id="leaderName">No teams yet</div>
        <div style="font-size:13px;color:#dbeafe" id="leaderScoreSnap">0 points</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:6px;align-items:flex-end">
        <span class="budget-pill">💰 <span id="leaderCoins">50</span> coins</span>
        <div class="streak-pill" id="streakPill" style="display:none">🔥 <span id="streakDays">0</span>-day streak</div>
      </div>
    </div>
    <div class="mini">
      <p><strong style="color:var(--heading)">Scoring:</strong> TODO summarise in one line.</p>
      <div class="kbd-help">
        <span><kbd>Space</kbd> start</span>
        <span><kbd>?</kbd> shortcuts</span>
      </div>
      <div class="settings-row">
        <label><input type="checkbox" id="hcToggle"/> High-contrast</label>
        <button class="btn ghost btn-sm" id="cheatBtn">⌨ Shortcuts</button>
        <span class="autosave" id="autosaveLabel">Saved just now</span>
      </div>
    </div>
  </aside>
</section>

<div class="flow">
  {flow_steps}
</div>

<section class="grid">

<aside class="setup-panel panel" id="setupPanel">
  <h2 style="margin-bottom:6px">Custom Setup</h2>
  <p class="hint" style="margin:0 0 12px">Three quick steps. Or just hit <strong>Play Demo Now</strong>.</p>

  <div class="setup-section">
    <div class="setup-section-head"><span class="sec-ico">1</span><h3>Quick start</h3><span class="step">Optional</span></div>
    <div class="quickstart">
      <button class="btn ghost" id="sampleBtn">↻ Use demo teams</button>
      <button class="btn ghost" id="saveTemplateBtn">⭑ Save as template</button>
    </div>
    <div id="templateList" style="display:flex;flex-wrap:wrap;gap:4px;margin-top:6px"></div>
  </div>

  <div class="setup-section">
    <div class="setup-section-head"><span class="sec-ico">2</span><h3>Game settings</h3><span class="step">Required</span></div>
    <div class="form-row">
      <label for="langSelect">Language</label>
      <select id="langSelect"></select>
    </div>
    <div class="setup-grid-2">
      <!-- TODO: 2-4 game-specific selects (round time, mode, difficulty, etc.) -->
      <div class="form-row">
        <label for="timeSelect">Round time</label>
        <select id="timeSelect">
          <option value="30">30 seconds</option>
          <option value="45" selected>45 seconds</option>
          <option value="60">60 seconds</option>
          <option value="90">90 seconds</option>
        </select>
      </div>
    </div>
    <div class="estimator" id="setupEstimator">
      <span class="ico">⏱</span>
      <div>Session: <strong id="estTime">~9 min</strong></div>
    </div>
  </div>

  <div class="setup-section">
    <div class="setup-section-head"><span class="sec-ico">3</span><h3>Teams</h3><span class="step">Required</span></div>
    <div class="add-team-form">
      <div class="name-row">
        <input id="teamName" placeholder="Team name" aria-label="Team name"/>
        <button class="btn btn-sm" id="addTeamBtn">+ Add</button>
      </div>
      <textarea id="teamMembers" placeholder="Members (optional, comma-separated)"></textarea>
    </div>
    <div class="team-list-head"><h3 style="margin:0;font-size:13px">Roster</h3><small id="rosterCount">0 teams</small></div>
    <div class="team-list" id="teamList"><div class="empty">Add your first team, load demo teams, or click Play Demo Now.</div></div>
  </div>

  <div class="start-cta">
    <button class="btn success" id="startGameBtn">▶ Start Game</button>
    <span class="help" id="startCtaHelp">Add at least 1 team to start.</span>
  </div>
</aside>

<main class="game-board" id="gameArea">
  <div class="status">
    <div><strong id="statusTitle">Ready to play</strong><br/><span id="statusSub">Click Play Demo Now or add teams.</span></div>
    <div class="timer" id="timer">⏱ 00:00</div>
    <div class="status-progress" aria-hidden="true"><span class="status-progress-fill" id="statusProgressFill"></span></div>
  </div>

  <section class="panel">
    <div class="tabs">
      <button class="tab active" data-view="play">▶ Play <span class="kbd">P</span></button>
      <button class="tab" data-view="leaderboard">🏆 Leaderboard <span class="kbd">L</span></button>
      <button class="tab" data-view="review">💬 Review <span class="kbd">R</span></button>
      <button class="tab" data-view="awards">🎖 Awards <span class="kbd">A</span></button>
      <button class="tab" data-view="log">📋 Round Log</button>
    </div>

    <div id="playView">
      <!-- TODO: build the gameplay surface here (stage, controls, side panel) -->
      <div class="empty">TODO: implement the gameplay UI for {title}.</div>
    </div>

    <div id="leaderboardView" class="hidden">
      <h2>Leaderboard <span class="live-badge">Live</span></h2>
      <div class="leaderboard" id="leaderboard"></div>
    </div>

    <div id="reviewView" class="hidden">
      <h2>Auto Review</h2>
      <div id="reviewContent"></div>
      <div class="actions" style="margin-top:14px">
        <button class="btn" id="exportBtn">📥 Export JSON</button>
        <button class="btn secondary" id="exportCsvBtn">📊 Export CSV</button>
        <button class="btn secondary" id="shareBtn">🔗 Share session</button>
        <button class="btn secondary" id="reminderBtn">📅 14-day reminder</button>
        <button class="btn ghost" onclick="window.print()">🖨 Print / PDF</button>
      </div>
    </div>

    <div id="awardsView" class="hidden">
      <h2>Awards &amp; badges</h2>
      <div class="awards-grid" id="awardsList"></div>
    </div>

    <div id="logView" class="hidden">
      <h2>Round Log</h2>
      <div class="log" id="roundLog"></div>
    </div>
  </section>
</main>

</section>

<div class="footer-note">Standalone prototype · runs fully in the browser · no backend, login, or internet required after download.</div>

</div>

<!-- How to play -->
<div class="overlay" id="howOverlay" role="dialog" aria-modal="true">
  <div class="overlay-modal">
    <div class="overlay-head"><div><h2>How to Play {title}</h2><p>TODO: subtitle</p></div><button class="close" id="closeHow">×</button></div>
    <div class="overlay-body">
      <div class="how-steps">
        <div class="how-step"><div class="how-icon">1</div><strong>Step 1</strong><span>TODO</span></div>
        <div class="how-step"><div class="how-icon">2</div><strong>Step 2</strong><span>TODO</span></div>
        <div class="how-step"><div class="how-icon">3</div><strong>Step 3</strong><span>TODO</span></div>
        <div class="how-step"><div class="how-icon">4</div><strong>Step 4</strong><span>TODO</span></div>
      </div>
      <div class="actions" style="margin-top:16px">
        <button class="btn success" id="howDemo">▶ Start Demo</button>
        <button class="btn ghost" id="howClose2">Close Guide</button>
      </div>
    </div>
  </div>
</div>

<!-- Cheat sheet -->
<div class="overlay" id="cheatOverlay" role="dialog" aria-modal="true">
  <div class="overlay-modal">
    <div class="overlay-head"><div><h2>⌨ Keyboard &amp; Game Cheat Sheet</h2></div><button class="close" id="cheatClose">×</button></div>
    <div class="overlay-body">
      <div class="cheat-grid">
        <div class="cheat-section"><h4>Keyboard shortcuts</h4>
          <div class="cheat-row"><span class="lbl">Start round</span><kbd>Space</kbd></div>
          <div class="cheat-row"><span class="lbl">Cheat sheet</span><kbd>?</kbd></div>
          <div class="cheat-row"><span class="lbl">Close modal</span><kbd>Esc</kbd></div>
        </div>
        <!-- TODO: add game-specific cheat sections (rules, events, badges, modes, a11y) -->
      </div>
      <div class="actions"><button class="btn ghost" id="cheatCloseBottom">Close</button></div>
    </div>
  </div>
</div>

<!-- Round summary -->
<div class="overlay" id="summaryOverlay" role="dialog" aria-modal="true">
  <div class="overlay-modal">
    <div class="summary-winner"><div class="crown">👑</div><h2 id="summaryWinnerName">Round winner</h2><p style="margin:4px 0 0;color:#3a2700;font-weight:800" id="summaryWinnerScore">0 points</p></div>
    <div class="summary-grid" id="summaryGrid"></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;padding:0 24px 24px;justify-content:flex-end">
      <button class="btn ghost" id="summaryClose">Close</button>
      <button class="btn warning" id="summaryNext">→ Next round</button>
    </div>
  </div>
</div>

<!-- Share modal -->
<div class="overlay" id="shareOverlay" role="dialog" aria-modal="true">
  <div class="overlay-modal">
    <div class="overlay-head"><div><h2>Share this session</h2><p>Shareable URL encodes the session state. No backend.</p></div><button class="close" id="shareClose">×</button></div>
    <div class="overlay-body">
      <label style="display:block;margin-bottom:6px;font-weight:900">Shareable URL</label>
      <div class="share-box"><input id="shareUrl" readonly value=""/><button class="btn btn-sm" id="copyShareUrl">📋 Copy</button></div>
      <label style="display:block;margin-bottom:6px;font-weight:900;margin-top:14px">Slack / Teams card</label>
      <div class="share-box" style="display:block">
        <p id="slackCard" style="margin:0;line-height:1.55;font-size:13.5px;white-space:pre-line"></p>
        <button class="btn btn-sm" id="copySlackCard" style="margin-top:8px">📋 Copy card text</button>
      </div>
      <label style="display:block;margin-bottom:6px;font-weight:900;margin-top:14px">Embed snippet</label>
      <div class="share-box"><input id="embedSnippet" readonly value=""/><button class="btn btn-sm" id="copyEmbed">📋 Copy</button></div>
      <div class="share-row" style="margin-top:14px">
        <button class="btn warning" id="presenterModeBtn">📺 Open Presenter View</button>
        <button class="btn warning" id="playerModeBtn">📱 Open Player View</button>
      </div>
    </div>
  </div>
</div>

<div class="undo-banner" id="undoBanner" role="status" aria-live="polite">
  <span id="undoText">Round saved.</span>
  <button id="undoBtn">↶ Undo</button>
</div>

<canvas id="confetti" aria-hidden="true"></canvas>
<div class="toast" id="toast">Ready</div>

<script src="_shared/shell.js"></script>
<script>
/* ===========================================================
   {title.upper()} - Edstellar Engage
   Game-specific logic. Shared utilities are in EngageShell.
=========================================================== */
const Shell = window.EngageShell;
const {{ $, safe, makeId }} = Shell;

const STORAGE_KEY = '{storage}';
const HC_KEY = '{storage.replace("V1", "HC")}';
const STREAK_KEYS = {{ last: '{storage.replace("V1", "LastSession")}', streak: '{storage.replace("V1", "Streak")}' }};
const SEEN_KEY = '{storage.replace("V1", "HowSeen")}';

/* TODO: fill in your game's data */
const SAMPLE_TEAMS = [
  {{name:'Innovators', members:'Asha, Ravi'}},
  {{name:'Pioneers',   members:'Meera, Nikhil'}},
  {{name:'Catalysts',  members:'Sara, Arjun'}}
];

const BADGES = [
  {{id:'winner',  icon:'🏆', name:'Overall Winner', desc:'Highest total score', check:(p,all)=> all.sort((a,b)=>b.score-a.score)[0]?.id===p.id && p.score>0}},
  {{id:'first',   icon:'🥇', name:'First Win',      desc:'Won round 1',         check:(p)=> !!p.firstWin}},
  {{id:'champion',icon:'👑', name:'Champion',       desc:'Won the game',        check:(p)=> (p.badges||[]).includes('champion')}}
  /* TODO: add 7 more game-specific badges */
];

/* TODO: define your plot twists / random events array */
const EVENTS = [];

/* ---------- State ---------- */
let teams = [];
let round = 0;
let maxRounds = 3;
let phase = 'setup';
let log = [];
let sessionTemplates = [];
let currentLanguage = 'en';
let editingTeamId = null;
let lastSaveAt = 0;
let undoSnapshot = null;

function defaultTeam(name, members=''){{
  const i = teams.length;
  return {{
    id: makeId(), name, members,
    color: Shell.TEAM_COLORS[i % 8], avatar: Shell.TEAM_AVATARS[i % 8],
    score:0, coins:50, badges:[], firstWin:false
    /* TODO: add game-specific per-team fields */
  }};
}}

function saveState(){{ localStorage.setItem(STORAGE_KEY, JSON.stringify({{teams, round, maxRounds, phase, log, sessionTemplates, currentLanguage}})); lastSaveAt = Date.now(); }}
function loadState(){{ try{{ const s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}'); Object.assign({{teams, round, maxRounds, phase, log, sessionTemplates, currentLanguage}}, s); teams = s.teams || []; round = s.round || 0; maxRounds = s.maxRounds || 3; phase = s.phase || 'setup'; log = s.log || []; sessionTemplates = s.sessionTemplates || []; currentLanguage = s.currentLanguage || 'en'; }} catch(e){{}} }}

function setPhase(p){{ phase = p; Shell.setPhase(p, [{phases_js}]); saveState(); }}

function loadSampleTeams(){{
  teams = SAMPLE_TEAMS.map(d => {{ const t = defaultTeam(d.name, d.members); return t; }});
  saveState(); render(); Shell.toast('Sample teams loaded', 'success');
}}

function addTeam(){{
  const name = $('teamName').value.trim();
  if(!name) return Shell.toast('Add a team name', 'warning');
  teams.push(defaultTeam(name, $('teamMembers').value.trim()));
  $('teamName').value=''; $('teamMembers').value='';
  saveState(); render(); Shell.toast('Team added', 'success');
}}
function removeTeam(id){{ teams = teams.filter(t => t.id !== id); saveState(); render(); }}
function editTeam(id){{ editingTeamId = editingTeamId === id ? null : id; renderTeams(); }}
function setTeamColor(id, c){{ const t=teams.find(x=>x.id===id); if(t){{ t.color=c; saveState(); renderTeams(); }} }}
function setTeamAvatar(id, a){{ const t=teams.find(x=>x.id===id); if(t){{ t.avatar=a; saveState(); renderTeams(); }} }}
function saveTeamEdit(id){{ const t=teams.find(x=>x.id===id); if(!t) return; t.name = $('edit-name-'+id)?.value.trim() || t.name; t.members = $('edit-mem-'+id)?.value.trim() || t.members; editingTeamId = null; saveState(); render(); }}

function renderTeams(){{
  const host = $('teamList');
  if(!teams.length){{ host.innerHTML='<div class="empty">Add your first team or click Play Demo Now.</div>'; return; }}
  host.innerHTML = teams.map(t => {{
    const edit = editingTeamId === t.id ? `
      <div class="team-edit">
        <h4>Customize team</h4>
        <div class="form-row"><label>Name</label><input id="edit-name-${{t.id}}" value="${{safe(t.name)}}"></div>
        <div class="form-row"><label>Members</label><textarea id="edit-mem-${{t.id}}">${{safe(t.members||'')}}</textarea></div>
        <div class="swatch-row">${{Shell.TEAM_COLORS.map(c=>`<button class="swatch ${{t.color===c?'active':''}}" style="background:${{c}}" onclick="setTeamColor('${{t.id}}','${{c}}')"></button>`).join('')}}</div>
        <div class="avatar-row">${{Shell.TEAM_AVATARS.map(a=>`<button class="avatar-pick ${{t.avatar===a?'active':''}}" onclick="setTeamAvatar('${{t.id}}','${{a}}')">${{a}}</button>`).join('')}}</div>
        <div class="edit-actions"><button class="btn ghost btn-sm" onclick="editTeam('${{t.id}}')">Cancel</button><button class="btn btn-sm" onclick="saveTeamEdit('${{t.id}}')">Save</button></div>
      </div>` : '';
    return `<div class="team-item" style="--team-color:${{t.color}}">
      <div class="team-avatar" style="background:${{t.color}}">${{t.avatar}}</div>
      <div class="team-info">
        <div class="team-name">${{safe(t.name)}}</div>
        <div class="team-meta">${{safe(t.members||'No members')}} · ${{t.score}} pts · 💰 ${{t.coins}}</div>
        ${{edit}}
      </div>
      <div class="team-actions">
        <button class="team-btn" onclick="editTeam('${{t.id}}')">✎</button>
        <button class="delete-team" onclick="removeTeam('${{t.id}}')">×</button>
      </div>
    </div>`;
  }}).join('');
}}

/* TODO: implement these */
function startRound(){{ Shell.toast('TODO: implement startRound()', 'warning'); }}
function reveal(){{ Shell.toast('TODO: implement reveal()', 'warning'); }}
function renderPlay(){{ /* TODO */ }}

function renderLeaderboard(){{
  const sorted = [...teams].sort((a,b)=>b.score-a.score);
  $('leaderboard').innerHTML = sorted.length ? sorted.map((p,i)=>{{
    const cls = i===0?'rank-1':i===1?'rank-2':i===2?'rank-3':'';
    return `<div class="leader-item ${{cls}}" style="--team-color:${{p.color}}">
      <div class="rank">${{i+1}}</div>
      <div class="team-avatar" style="background:${{p.color}};width:38px;height:38px;font-size:18px;border-radius:12px">${{p.avatar}}</div>
      <div><div class="team-name">${{safe(p.name)}}</div><div class="team-meta">${{safe(p.members||'')}} · 💰 ${{p.coins}}</div></div>
      <div class="leader-score">${{p.score}}<small>points</small></div>
    </div>`;
  }}).join('') : '<div class="empty">No teams yet.</div>';
}}
function renderReview(){{ const last = log[log.length-1]; $('reviewContent').innerHTML = last ? `<div class="panel" style="padding:18px"><h3>Round ${{last.round}}</h3><p>${{safe(last.summary||'')}}</p></div>` : '<div class="empty">No review yet.</div>'; }}
function renderAwards(){{
  if(!teams.length){{ $('awardsList').innerHTML='<div class="empty">No awards yet.</div>'; return; }}
  $('awardsList').innerHTML = BADGES.map(b => {{
    const winners = teams.filter(p => {{ try{{ return b.check(p, teams); }} catch(e){{ return false; }} }});
    const earned = winners.length > 0;
    return `<div class="award-card ${{earned?'earned':'locked'}}"><div class="award-icon">${{b.icon}}</div><div class="award-name">${{b.name}}</div><div class="award-desc">${{b.desc}}</div><div class="award-by">${{earned ? winners.slice(0,2).map(w=>safe(w.name)).join(', ') : 'Locked'}}</div></div>`;
  }}).join('');
}}
function renderLog(){{ $('roundLog').innerHTML = log.length ? log.slice().reverse().map(x => `<div class="log-item"><div class="team-name">Round ${{x.round}}</div><div class="team-meta">${{new Date(x.time).toLocaleString()}}</div><p>${{safe(x.summary||'')}}</p></div>`).join('') : '<div class="empty">No completed rounds yet.</div>'; }}

function updateEstimator(){{ $('estTime').textContent = teams.length ? '~' + Math.max(1, Math.round(teams.length * maxRounds * 1.5)) + ' min' : '~9 min'; }}
function updateRosterCount(){{ $('rosterCount').textContent = teams.length + (teams.length===1?' team':' teams'); }}
function updateStartCta(){{
  const btn = $('startGameBtn'); const help = $('startCtaHelp');
  const ready = teams.length >= 1;
  btn.disabled = !ready;
  btn.textContent = ready ? '▶ Start Game · '+teams.length+(teams.length===1?' team':' teams') : '▶ Start Game';
  help.textContent = ready ? $('estTime')?.textContent + ' total' : 'Add at least 1 team to start.';
}}
function renderSnapshot(){{
  $('teamCount').textContent = teams.length;
  $('roundCount').textContent = round + ' / ' + maxRounds;
  document.body.dataset.teams = String(teams.length);
  document.body.dataset.roundsPlayed = String(log.length);
  const leader = [...teams].sort((a,b)=>b.score-a.score)[0];
  $('leaderName').textContent = leader?.name || 'No teams yet';
  $('leaderScoreSnap').textContent = (leader?.score||0) + ' points';
  $('leaderCoins').textContent = leader?.coins || 50;
}}
function render(){{ renderSnapshot(); renderTeams(); renderPlay(); renderLeaderboard(); renderReview(); renderAwards(); renderLog(); renderTemplates(); Shell.setPhase(phase, [{phases_js}]); updateEstimator(); updateRosterCount(); updateStartCta(); }}

const viewSwitcher = Shell.makeViewSwitcher(['play','leaderboard','review','awards','log'], {{ onSwitch: v => {{ if(v==='awards') renderAwards(); }} }});

function openHow(){{ $('howOverlay').classList.add('show'); }} function closeHow(){{ $('howOverlay').classList.remove('show'); }}
function openCheat(){{ $('cheatOverlay').classList.add('show'); }} function closeCheat(){{ $('cheatOverlay').classList.remove('show'); }}
function closeSummary(){{ $('summaryOverlay').classList.remove('show'); }}

function buildShareState(){{ return {{teams, log, language:currentLanguage, round, maxRounds}}; }}
function openShare(){{
  $('shareUrl').value = Shell.buildShareLink(buildShareState());
  const champ = [...teams].sort((a,b)=>b.score-a.score)[0];
  $('slackCard').textContent = `:trophy: *{title} - Edstellar Engage*\\n${{champ?`Leader: *${{champ.name}}* with *${{champ.score}} pts*`:'Game in progress'}}\\nReplay: ${{$('shareUrl').value}}`;
  $('embedSnippet').value = Shell.buildEmbed();
  $('shareOverlay').classList.add('show');
}}
function closeShare(){{ $('shareOverlay').classList.remove('show'); }}

function exportReport(){{ Shell.download('{slug}-report.json', JSON.stringify({{game:'{title}', exportedAt:new Date().toISOString(), teams, log}}, null, 2)); Shell.toast('Report exported', 'success'); }}
function exportCsv(){{ const rows = [['round','summary','time']]; log.forEach(x => rows.push([x.round, x.summary||'', x.time])); Shell.exportCsv('{slug}-log.csv', rows); }}

function saveSessionTemplate(){{ const name = prompt('Template name?', 'Quick Game'); if(!name) return; sessionTemplates.push({{id:makeId(), name, time:$('timeSelect').value, language:currentLanguage}}); saveState(); renderTemplates(); Shell.toast('Template saved', 'success'); }}
function loadSessionTemplate(id){{ const t = sessionTemplates.find(x => x.id === id); if(!t) return; $('timeSelect').value = t.time; if(t.language) setLang(t.language); saveState(); updateEstimator(); Shell.toast('Loaded: '+t.name); }}
function deleteSessionTemplate(id){{ sessionTemplates = sessionTemplates.filter(t => t.id !== id); saveState(); renderTemplates(); }}
function renderTemplates(){{ const host = $('templateList'); if(!host) return; host.innerHTML = sessionTemplates.length ? sessionTemplates.map(t => `<span class="template-pill" onclick="loadSessionTemplate('${{t.id}}')">${{safe(t.name)}}<span class="x" onclick="event.stopPropagation();deleteSessionTemplate('${{t.id}}')">×</span></span>`).join('') : '<span class="hint" style="margin:0">No saved templates yet.</span>'; }}

function setLang(lang){{ currentLanguage = lang; Shell.setLanguage(lang); saveState(); }}

function reset(){{
  Shell.confirmReset({{
    storageKey: STORAGE_KEY,
    onReset: () => {{
      Shell.stopTimer();
      teams = []; round = 0; phase = 'setup'; log = []; undoSnapshot = null; editingTeamId = null;
      $('timer').textContent = '⏱ 00:00';
      $('statusTitle').textContent = 'Ready to play';
      $('statusSub').textContent = 'Click Play Demo Now or add teams.';
      render(); viewSwitcher.switchView('play');
    }}
  }});
}}

/* ---------- Wire up ---------- */
$('langSelect').innerHTML = Shell.languageOptionsHtml(currentLanguage);

$('demoBtn').onclick = () => {{ Shell.fullscreen(); if(!teams.length) loadSampleTeams(); startRound(); }};
$('setupBtn').onclick = () => {{ $('setupPanel').scrollIntoView({{behavior:'smooth'}}); setPhase('setup'); }};
$('howBtn').onclick = openHow; $('closeHow').onclick = closeHow; $('howClose2').onclick = closeHow;
$('howDemo').onclick = () => {{ closeHow(); Shell.fullscreen(); if(!teams.length) loadSampleTeams(); startRound(); }};
$('howOverlay').onclick = e => {{ if(e.target.id==='howOverlay') closeHow(); }};
$('sampleBtn').onclick = loadSampleTeams;
$('addTeamBtn').onclick = addTeam;
$('teamName').addEventListener('keydown', e => {{ if(e.key==='Enter') addTeam(); }});
$('resetBtn').onclick = reset;
$('saveTemplateBtn').onclick = saveSessionTemplate;
$('langSelect').addEventListener('change', e => setLang(e.target.value));
$('timeSelect')?.addEventListener('change', () => {{ updateEstimator(); updateStartCta(); saveState(); }});
$('startGameBtn').onclick = () => {{ if(!teams.length) return Shell.toast('Add a team first','warning'); startRound(); }};
$('exportBtn').onclick = exportReport;
$('exportCsvBtn').onclick = exportCsv;
$('shareBtn').onclick = openShare;
$('reminderBtn').onclick = () => Shell.downloadIcs({{summary:'{title} - Reinforcement Session', filename:'{slug}-reminder.ics'}});
$('cheatBtn').onclick = openCheat;
$('cheatClose').onclick = closeCheat;
$('cheatCloseBottom').onclick = closeCheat;
$('cheatOverlay').onclick = e => {{ if(e.target.id==='cheatOverlay') closeCheat(); }};
$('shareClose').onclick = closeShare;
$('shareOverlay').onclick = e => {{ if(e.target.id==='shareOverlay') closeShare(); }};
$('copyShareUrl').onclick = () => Shell.copy($('shareUrl').value);
$('copySlackCard').onclick = () => Shell.copy($('slackCard').textContent);
$('copyEmbed').onclick = () => Shell.copy($('embedSnippet').value);
$('presenterModeBtn').onclick = () => window.open(location.pathname+'?mode=present','_blank');
$('playerModeBtn').onclick = () => window.open(location.pathname+'?mode=play','_blank');
$('summaryClose').onclick = closeSummary;
$('summaryNext').onclick = () => {{ closeSummary(); /* TODO: nextRound() */ }};
$('hcToggle').addEventListener('change', e => Shell.applyHc(e.target.checked, HC_KEY));
document.querySelectorAll('.tab').forEach(t => t.onclick = () => viewSwitcher.switchView(t.dataset.view));

Shell.bindKeys({{
  escape: () => {{ closeHow(); closeCheat(); closeShare(); closeSummary(); }},
  '?': openCheat,
  space: startRound,
  p: () => viewSwitcher.switchView('play'),
  l: () => viewSwitcher.switchView('leaderboard'),
  r: () => viewSwitcher.switchView('review'),
  a: () => viewSwitcher.switchView('awards')
  /* TODO: add game-specific shortcuts (D, E, N, T, etc.) */
}});

/* Boot */
Shell.detectMode();
const fromHash = Shell.loadFromHash();
if(fromHash){{ Object.assign({{teams, log, round, maxRounds}}, fromHash); teams = fromHash.teams || teams; log = fromHash.log || []; round = fromHash.round || 0; maxRounds = fromHash.maxRounds || 3; currentLanguage = fromHash.language || 'en'; Shell.toast('Loaded shared session', 'success'); }}
else {{ loadState(); }}
Shell.updateStreak(STREAK_KEYS);
setLang(currentLanguage);
Shell.bindAutosaveLabel(() => lastSaveAt);
render();
Shell.applyHc(localStorage.getItem(HC_KEY) === '1', HC_KEY);
if(!localStorage.getItem(SEEN_KEY) && !document.body.classList.contains('mode-present') && !document.body.classList.contains('mode-play')){{ setTimeout(openHow, 450); localStorage.setItem(SEEN_KEY, '1'); }}
</script>
</body>
</html>
"""


def register_in_parser(slug: str) -> None:
    """Append slug to PLAYABLE dict in parse_master.py."""
    text = PARSE_MASTER.read_text(encoding="utf-8")
    if f'"{slug}":' in text:
        print(f"  {slug} already in PLAYABLE")
        return
    pattern = re.compile(r'(PLAYABLE\s*=\s*\{[^}]*?)(\n\})', re.S)
    m = pattern.search(text)
    if not m:
        print("  could not find PLAYABLE block; skipping", file=sys.stderr)
        return
    new_block = m.group(1).rstrip() + f',\n    "{slug}": "./play/{slug}.html"' + m.group(2)
    PARSE_MASTER.write_text(text[:m.start()] + new_block + text[m.end():], encoding="utf-8")
    print(f"  added {slug} to PLAYABLE in parse_master.py")


def main():
    ap = argparse.ArgumentParser(description="Scaffold a new Edstellar Engage game.")
    ap.add_argument("slug", help="URL slug, e.g. trust-fall")
    ap.add_argument("title", help='Game title, e.g. "Trust Fall"')
    ap.add_argument("--phases", default="setup,build,event,score,review",
                    help="Comma-separated 5 phase names for the flow stepper")
    ap.add_argument("--register", action="store_true",
                    help="Also append slug to PLAYABLE and regenerate games.json")
    args = ap.parse_args()

    slug = re.sub(r"[^a-z0-9-]", "-", args.slug.lower()).strip("-")
    phases = [p.strip() for p in args.phases.split(",") if p.strip()]
    if len(phases) != 5:
        print(f"Warning: {len(phases)} phases provided, expected 5 for the standard flow.", file=sys.stderr)

    out = PLAY_DIR / f"{slug}.html"
    if out.exists():
        print(f"Refusing to overwrite existing {out.relative_to(ROOT)}", file=sys.stderr)
        sys.exit(1)
    out.write_text(render_html(slug, args.title, phases), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
    print(f"  Storage key: {slug_to_storage(slug)}")
    print(f"  Phases:      {' -> '.join(phases)}")

    if args.register:
        register_in_parser(slug)
        print("Regenerating games.json...")
        subprocess.run([sys.executable, str(PARSE_MASTER)], check=True)

    print()
    print("Next steps:")
    print(f"  1. Open {out.relative_to(ROOT)} in your editor and search for 'TODO'")
    print(f"  2. Fill in: gameplay UI in #playView, startRound/reveal logic,")
    print(f"     BADGES (10), EVENTS / plot twists, scoring rules, cheat sheet")
    print(f"  3. Test by opening from file:// or via Vercel deploy")
    print(f"  4. Re-run python engage-prototype/_build/parse_master.py after registering")


if __name__ == "__main__":
    main()
