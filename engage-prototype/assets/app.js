/* Edstellar Engage prototype — vanilla JS.
   Pages: landing | library | detail. Driven by data in games-data.js (window.GAMES_DATA).
   No framework, no build step, works from file:// because data is a script tag.
*/

// ---------- Data ----------
const DATA_URL = './assets/games.json';
let CACHE = null;
async function loadGames(){
  if(CACHE) return CACHE;
  if(window.GAMES_DATA && Array.isArray(window.GAMES_DATA.games)){
    CACHE = window.GAMES_DATA.games;
    return CACHE;
  }
  try{
    const r = await fetch(DATA_URL);
    const j = await r.json();
    CACHE = j.games || [];
    return CACHE;
  }catch(err){
    console.error('Could not load games. Include games-data.js before app.js if opening via file://.', err);
    return [];
  }
}

function escapeHtml(s){
  return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// ---------- Category icon + color ----------
const CAT_META = {
  'Leadership':       {bg:'linear-gradient(135deg,#0E2A47,#1E40AF)', icon:'crown'},
  'Communication':    {bg:'linear-gradient(135deg,#0F766E,#16B8A6)', icon:'chat'},
  'Critical Thinking':{bg:'linear-gradient(135deg,#7C3AED,#A855F7)', icon:'brain'},
  'Problem Solving':  {bg:'linear-gradient(135deg,#0EA5E9,#22D3EE)', icon:'puzzle'},
  'Decision Making':  {bg:'linear-gradient(135deg,#9333EA,#06B6D4)', icon:'compass'},
  'Time Management':  {bg:'linear-gradient(135deg,#0E2A47,#3B82F6)', icon:'clock'},
  'Goal Setting':     {bg:'linear-gradient(135deg,#DB2777,#F59E0B)', icon:'target'},
  'Performance Management':{bg:'linear-gradient(135deg,#0F766E,#84CC16)', icon:'chart'},
  'Accountability':   {bg:'linear-gradient(135deg,#1E40AF,#16B8A6)', icon:'handshake'},
  'Change Management':{bg:'linear-gradient(135deg,#7C3AED,#F472B6)', icon:'shuffle'},
  'Stress / Wellness':{bg:'linear-gradient(135deg,#16A34A,#84CC16)', icon:'leaf'},
  'Sales':            {bg:'linear-gradient(135deg,#0E2A47,#F59E0B)', icon:'megaphone'},
  'Customer Service': {bg:'linear-gradient(135deg,#0EA5E9,#16B8A6)', icon:'heart'},
  'HR / Onboarding':  {bg:'linear-gradient(135deg,#1D4ED8,#A855F7)', icon:'sparkle'}
};
const ICONS = {
  crown:    '<path d="M3 18h18l-2-9-4 4-3-7-3 7-4-4-2 9z" fill="currentColor"/><rect x="3" y="19" width="18" height="2" fill="currentColor" opacity=".5"/>',
  chat:     '<path d="M4 5h16v10H8l-4 4V5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="9" cy="10" r="1" fill="currentColor"/><circle cx="13" cy="10" r="1" fill="currentColor"/><circle cx="17" cy="10" r="1" fill="currentColor"/>',
  brain:    '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 1 4 3 3 0 0 0 3 4h3V4H9zm6 0a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-1 4 3 3 0 0 1-3 4h-3V4h2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
  puzzle:   '<path d="M5 5h6v3a2 2 0 0 0 4 0V5h4v6h-3a2 2 0 0 0 0 4h3v4h-6v-3a2 2 0 0 0-4 0v3H5v-6h3a2 2 0 0 0 0-4H5V5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
  compass:  '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 9l-2 5-4 1 2-5 4-1z" fill="currentColor"/>',
  clock:    '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  target:   '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="2" fill="currentColor"/>',
  chart:    '<path d="M4 20V8m6 12V4m6 16v-8m6 8V10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  handshake:'<path d="M3 13l4-4 3 3 4-4 4 4 3-3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 13l4 4 3-3 4 4 3-3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  shuffle:  '<path d="M3 7h4l10 10h4M3 17h4l10-10h4M17 5l4 2-4 2M17 15l4 2-4 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  leaf:     '<path d="M5 21c0-9 6-15 15-15-1 9-7 15-15 15z" fill="currentColor"/><path d="M5 21c4-4 8-8 14-14" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="1.5" stroke-linecap="round"/>',
  megaphone:'<path d="M3 10v4l10 5V5L3 10z" fill="currentColor"/><path d="M15 8c3 1 3 7 0 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  heart:    '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 5.5-7 10-7 10z" fill="currentColor"/>',
  sparkle:  '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2 2-6z" fill="currentColor"/>',
  // walkthrough step icons:
  lightbulb:'<path d="M9 18h6m-5 3h4M12 3a6 6 0 0 0-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 0 0-4-10z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>',
  play:     '<path d="M8 5v14l11-7L8 5z" fill="currentColor"/>',
  chatbox:  '<path d="M4 4h16v12H8l-4 4V4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8 10h8M8 13h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  star:     '<path d="M12 3l2.7 5.6 6.3.9-4.5 4.4 1.1 6.2L12 17l-5.6 3 1.1-6.2L3 9.5l6.3-.9L12 3z" fill="currentColor"/>'
};
function svgIcon(name, size=46){
  const path = ICONS[name] || ICONS.sparkle;
  return `<svg class="card-icon" width="${size}" height="${size}" viewBox="0 0 24 24" aria-hidden="true">${path}</svg>`;
}
function catBg(cat){ return (CAT_META[cat] || {bg:'linear-gradient(135deg,#0E2A47,#13355a)'}).bg; }
function catIcon(cat){ return (CAT_META[cat] || {icon:'sparkle'}).icon; }

// ---------- Card renderer ----------
function gameCard(g){
  const url = `./game.html?id=${encodeURIComponent(g.slug)}`;
  const ribbon = g.reinforcesTraining ? `<span class="card-ribbon" title="Reinforces an Edstellar training program">✓ Reinforces training</span>` : '';
  return `
  <a class="card" href="${url}" aria-label="View ${escapeHtml(g.title)}">
    <div class="card-thumb" style="--cat-bg:${catBg(g.category)}">
      <span class="card-cat-pill">${escapeHtml(g.category)}</span>
      ${ribbon}
      ${svgIcon(catIcon(g.category))}
    </div>
    <div class="card-body">
      <h3 class="card-title">${escapeHtml(g.title)}</h3>
      <p class="card-desc">${escapeHtml(g.concept || g.businessPurpose || '')}</p>
      <div class="badges">
        <span class="badge">${escapeHtml(g.duration)}</span>
        <span class="badge">${escapeHtml(g.format)}</span>
        <span class="badge badge-accent">${escapeHtml(g.difficulty)}</span>
      </div>
      <div class="card-foot">
        <span>👥 <strong>${escapeHtml(g.team)}</strong></span>
        ${g.economy ? `<span title="Uses in-game currency">🪙 EngageCoins</span>` : `<span>&nbsp;</span>`}
      </div>
    </div>
  </a>`;
}

function skeletonCards(n=6){
  return Array.from({length:n}).map(()=>`
    <div class="skel-card">
      <div class="sk sk-thumb"></div>
      <div class="sk-body">
        <div class="sk sk-line"></div>
        <div class="sk sk-line"></div>
        <div class="sk sk-line short"></div>
      </div>
    </div>`).join('');
}

// ---------- Library page ----------
const FILTERS = {
  category:new Set(), audience:new Set(), format:new Set(),
  teamBucket:new Set(), durationBucket:new Set(), difficulty:new Set(),
  reinforces:false, hasEconomy:false, search:'', sort:'popular'
};
const PAGE_SIZE = 12;
let CURRENT_PAGE = 1;

function readQuery(){
  const p = new URLSearchParams(location.search);
  const cat = p.get('category'); if(cat) FILTERS.category.add(cat);
  const aud = p.get('audience'); if(aud) FILTERS.audience.add(aud);
  const search = p.get('q'); if(search) FILTERS.search = search;
}

function gameMatches(g, except){
  // except: name of a filter group to ignore (so we can compute "what would happen if I toggled this on")
  const f = FILTERS;
  if(except!=='category' && f.category.size && !f.category.has(g.category)) return false;
  if(except!=='audience' && f.audience.size && !g.audience.some(a=>f.audience.has(a))) return false;
  if(except!=='format' && f.format.size && !f.format.has(g.format)) return false;
  if(except!=='teamBucket' && f.teamBucket.size && !f.teamBucket.has(g.teamBucket)) return false;
  if(except!=='durationBucket' && f.durationBucket.size && !f.durationBucket.has(g.durationBucket)) return false;
  if(except!=='difficulty' && f.difficulty.size && !f.difficulty.has(g.difficulty)) return false;
  if(except!=='reinforces' && f.reinforces && !g.reinforcesTraining) return false;
  if(except!=='hasEconomy' && f.hasEconomy && !g.economy) return false;
  if(f.search){
    const q = f.search.toLowerCase();
    const blob = [g.title,g.category,g.concept,g.businessPurpose,(g.skills||[]).join(' '),(g.audience||[]).join(' ')].join(' ').toLowerCase();
    if(!blob.includes(q)) return false;
  }
  return true;
}

function applyFilters(games){
  let out = games.filter(g => gameMatches(g));
  const order = {'<15':0,'15-30':1,'30-60':2,'60+':3};
  switch(FILTERS.sort){
    case 'shortest': out.sort((a,b)=>(order[a.durationBucket]??9)-(order[b.durationBucket]??9)); break;
    case 'az':       out.sort((a,b)=>a.title.localeCompare(b.title)); break;
    case 'reinforce':out.sort((a,b)=>(b.reinforcesTraining?1:0)-(a.reinforcesTraining?1:0)); break;
    default: /* popular = original order */ break;
  }
  return out;
}

// Count of games that would match if you toggled a specific chip on (and nothing else changed)
function chipCount(games, setName, value){
  const f = FILTERS;
  const set = f[setName];
  if(set instanceof Set && set.has(value)){
    // already active → show how many it currently contributes
    return games.filter(g => gameMatches(g)).length;
  }
  // hypothetically add this value
  const prev = set instanceof Set ? new Set(set) : null;
  if(set instanceof Set) set.add(value);
  const n = games.filter(g => gameMatches(g)).length;
  if(prev) f[setName] = prev;
  return n;
}

function buildChip(label, value, setName, count){
  const set = FILTERS[setName];
  const active = set.has(value) ? 'active' : '';
  const disabled = count===0 && !set.has(value) ? 'disabled' : '';
  return `<button class="chip ${active} ${disabled}" ${disabled?'disabled':''} data-set="${setName}" data-value="${escapeHtml(value)}">
    <span>${escapeHtml(label)}</span><span class="chip-count">${count}</span>
  </button>`;
}

const FILTER_DEFS = {
  category: ['Leadership','Communication','Critical Thinking','Problem Solving','Decision Making','Time Management','Goal Setting','Performance Management','Accountability','Change Management','Stress / Wellness','Sales','Customer Service','HR / Onboarding'],
  audience: ['All employees','Sales','Customer Service','Leaders','Managers','New hires'],
  format:   ['Live','Async','Hybrid','Facilitated'],
  teamBucket:[['Solo','1'],['Small (2-10)','2-10'],['Medium (10-50)','10-50'],['Large (50+)','50+']],
  durationBucket:[['Under 15 min','<15'],['15-30 min','15-30'],['30-60 min','30-60'],['60+ min','60+']],
  difficulty:['Easy','Medium','Hard']
};

async function renderFilters(){
  const host = document.getElementById('filters'); if(!host) return;
  const games = await loadGames();
  const block = (title, key, values) => {
    const items = values.map(v => {
      const [lab, val] = Array.isArray(v) ? v : [v, v];
      const n = chipCount(games, key, val);
      return buildChip(lab, val, key, n);
    }).join('');
    return `<div class="filter-group">
      <div class="filter-title"><span>${title}</span><button class="filter-clear" data-clear="${key}">Clear</button></div>
      <div>${items}</div>
    </div>`;
  };
  host.innerHTML = `
    ${block('Category','category', FILTER_DEFS.category)}
    ${block('Audience','audience', FILTER_DEFS.audience)}
    ${block('Format','format', FILTER_DEFS.format)}
    ${block('Team size','teamBucket', FILTER_DEFS.teamBucket)}
    ${block('Duration','durationBucket', FILTER_DEFS.durationBucket)}
    ${block('Difficulty','difficulty', FILTER_DEFS.difficulty)}
    <div class="filter-group">
      <label class="toggle-row">
        <input type="checkbox" id="ft-reinforces" ${FILTERS.reinforces?'checked':''}/>
        Reinforces Edstellar training
      </label>
      <label class="toggle-row" style="margin-top:8px">
        <input type="checkbox" id="ft-economy" ${FILTERS.hasEconomy?'checked':''}/>
        Uses EngageCoins (in-game)
      </label>
    </div>
  `;

  host.querySelectorAll('[data-set]').forEach(btn=>{
    btn.addEventListener('click', async ()=>{
      const set = FILTERS[btn.dataset.set]; const val = btn.dataset.value;
      if(set.has(val)) set.delete(val); else set.add(val);
      await refreshLibrary();
    });
  });
  host.querySelectorAll('[data-clear]').forEach(btn=>{
    btn.addEventListener('click', async ()=>{
      FILTERS[btn.dataset.clear].clear();
      await refreshLibrary();
    });
  });
  host.querySelector('#ft-reinforces')?.addEventListener('change', async e=>{
    FILTERS.reinforces = e.target.checked; await refreshLibrary();
  });
  host.querySelector('#ft-economy')?.addEventListener('change', async e=>{
    FILTERS.hasEconomy = e.target.checked; await refreshLibrary();
  });
}

function renderSummary(){
  const host = document.getElementById('active-pills'); if(!host) return;
  const wrap = host.parentElement;
  const pills = [];
  ['category','audience','format','teamBucket','durationBucket','difficulty'].forEach(k=>{
    for(const v of FILTERS[k]) pills.push({k,v,label:v});
  });
  if(FILTERS.reinforces) pills.push({k:'reinforces',v:true,label:'Reinforces training'});
  if(FILTERS.hasEconomy) pills.push({k:'hasEconomy',v:true,label:'Uses EngageCoins'});
  if(FILTERS.search) pills.push({k:'search',v:FILTERS.search,label:`"${FILTERS.search}"`});

  if(!pills.length){ wrap?.classList.remove('has'); host.innerHTML = ''; return; }
  wrap?.classList.add('has');
  host.innerHTML = `<span class="summary-label">Filtering:</span>` + pills.map(p =>
    `<span class="active-pill">${escapeHtml(p.label)}<button aria-label="Remove ${escapeHtml(p.label)}" data-pill-key="${p.k}" data-pill-val="${escapeHtml(String(p.v))}">×</button></span>`
  ).join('') + `<button class="clear-all" id="clear-all">Clear all</button>`;
}

async function renderResults(){
  const games = await loadGames();
  const filtered = applyFilters(games);
  const grid = document.getElementById('grid-results');
  const count = document.getElementById('result-count');

  // Pagination math
  const total = filtered.length;
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  if(CURRENT_PAGE > totalPages) CURRENT_PAGE = totalPages;
  if(CURRENT_PAGE < 1) CURRENT_PAGE = 1;
  const start = (CURRENT_PAGE - 1) * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, total);
  const slice = filtered.slice(start, end);

  if(count){
    const totalLabel = games.length >= 200 ? '200+' : String(games.length);
    if(total === 0){
      count.textContent = `0 of ${totalLabel} games`;
    } else if(total <= PAGE_SIZE){
      count.textContent = total === games.length
        ? `Browsing all ${totalLabel} games`
        : `Showing all ${total} matching games`;
    } else {
      count.textContent = `Showing ${start+1}–${end} of ${total} games`;
    }
  }
  if(!grid) return;

  if(!total){
    grid.innerHTML = `<div class="empty">
      <strong>No games match all those filters.</strong>
      Try removing one or <a href="#" id="reset-all">clear all filters</a>.
    </div>`;
    grid.querySelector('#reset-all')?.addEventListener('click', async e=>{
      e.preventDefault(); resetFilters(); await refreshLibrary();
    });
    renderPagination(0, 1);
    return;
  }

  grid.innerHTML = slice.map(gameCard).join('');
  renderPagination(totalPages, CURRENT_PAGE);
}

function renderPagination(totalPages, page){
  let host = document.getElementById('pager');
  if(!host){
    const grid = document.getElementById('grid-results');
    if(!grid) return;
    host = document.createElement('nav');
    host.id = 'pager'; host.className = 'pager'; host.setAttribute('aria-label','Pagination');
    grid.insertAdjacentElement('afterend', host);
  }
  if(totalPages <= 1){ host.innerHTML = ''; return; }

  // Build a windowed list: 1 … (p-1) p (p+1) … N
  const pages = [];
  const window2 = (n) => Math.max(2, Math.min(totalPages-1, n));
  pages.push(1);
  const left = window2(page - 1), right = window2(page + 1);
  if(left > 2) pages.push('…');
  for(let i=left; i<=right; i++) if(i>1 && i<totalPages) pages.push(i);
  if(right < totalPages-1) pages.push('…');
  if(totalPages > 1) pages.push(totalPages);

  const prevDisabled = page<=1 ? 'disabled' : '';
  const nextDisabled = page>=totalPages ? 'disabled' : '';

  host.innerHTML = `
    <button class="pg-btn" data-pg="prev" ${prevDisabled} aria-label="Previous page">← Prev</button>
    <div class="pg-pages">
      ${pages.map(p => p === '…'
        ? `<span class="pg-gap">…</span>`
        : `<button class="pg-num ${p===page?'active':''}" data-pg="${p}" ${p===page?'aria-current="page"':''}>${p}</button>`
      ).join('')}
    </div>
    <button class="pg-btn" data-pg="next" ${nextDisabled} aria-label="Next page">Next →</button>
  `;

  host.onclick = (e)=>{
    const btn = e.target.closest('[data-pg]'); if(!btn || btn.disabled) return;
    const v = btn.dataset.pg;
    if(v === 'prev') CURRENT_PAGE = Math.max(1, CURRENT_PAGE - 1);
    else if(v === 'next') CURRENT_PAGE = Math.min(totalPages, CURRENT_PAGE + 1);
    else CURRENT_PAGE = parseInt(v, 10);
    renderResults();
    document.getElementById('grid-results')?.scrollIntoView({behavior:'smooth', block:'start'});
  };
}

function resetFilters(){
  ['category','audience','format','teamBucket','durationBucket','difficulty'].forEach(k=>FILTERS[k].clear());
  FILTERS.reinforces=false; FILTERS.hasEconomy=false; FILTERS.search='';
  const s=document.getElementById('search-input'); if(s) s.value='';
}

async function refreshLibrary(){
  CURRENT_PAGE = 1;
  await renderFilters();
  renderSummary();
  await renderResults();
  document.dispatchEvent(new CustomEvent('engage:filters-changed'));
}

function initLibrary(){
  readQuery();
  // initial skeleton
  const grid = document.getElementById('grid-results');
  if(grid) grid.innerHTML = `<div style="grid-column:1/-1;display:grid;grid-template-columns:repeat(3,1fr);gap:18px">${skeletonCards(6)}</div>`;

  refreshLibrary();

  // Search with debounce + "/" focus shortcut
  const search = document.getElementById('search-input');
  if(search){
    if(FILTERS.search) search.value = FILTERS.search;
    let t; search.addEventListener('input', e=>{
      clearTimeout(t);
      t = setTimeout(async ()=>{ FILTERS.search = e.target.value.trim(); await refreshLibrary(); }, 140);
    });
    document.addEventListener('keydown', e=>{
      if(e.key==='/' && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA'){
        e.preventDefault(); search.focus();
      }
    });
  }

  const sort = document.getElementById('sort-select');
  sort?.addEventListener('change', async e=>{ FILTERS.sort = e.target.value; await renderResults(); });

  const toggle = document.getElementById('filters-toggle');
  toggle?.addEventListener('click', ()=>document.getElementById('filters').classList.toggle('open'));

  // Summary actions delegated
  document.addEventListener('click', async e=>{
    const btn = e.target.closest('[data-pill-key]');
    if(btn){
      const k = btn.dataset.pillKey;
      const v = btn.dataset.pillVal;
      if(k==='reinforces'){ FILTERS.reinforces=false; }
      else if(k==='hasEconomy'){ FILTERS.hasEconomy=false; }
      else if(k==='search'){ FILTERS.search=''; const s=document.getElementById('search-input'); if(s) s.value=''; }
      else { FILTERS[k].delete(v); }
      await refreshLibrary(); return;
    }
    if(e.target.id==='clear-all'){
      resetFilters();
      await refreshLibrary();
    }
  });
}

// ---------- Library help modal ----------
function initLibraryHelp(){
  injectHelpButton('Open library help');
  injectHelpModal('library-help', `
    <h3>How the Game Library works</h3>
    <p class="muted">215 games across 14 categories — built for HR, L&amp;D, managers, and team leads.</p>
    <ul class="help-list">
      <li><span class="help-num">1</span><div><strong>Search</strong><p>Type a game name, skill, or keyword — "escape", "onboarding", "negotiation". Results update as you type.</p></div></li>
      <li><span class="help-num">2</span><div><strong>Filter with live counts</strong><p>Each filter chip shows how many games would match if you toggled it on. Disabled chips mean no games match in your current selection.</p></div></li>
      <li><span class="help-num">3</span><div><strong>Sort smart</strong><p>"Most reinforcing" surfaces games tied to your training catalog first. "Shortest first" is great for quick energizers.</p></div></li>
      <li><span class="help-num">4</span><div><strong>Reinforcement toggle</strong><p>Turn on "Reinforces Edstellar training" to show only games designed as post-program reinforcement.</p></div></li>
      <li><span class="help-num">5</span><div><strong>Open any game</strong><p>Click a card to see the full concept, how to play, review questions, key takeaway, and currency model where applicable.</p></div></li>
    </ul>
    <div class="kbd-tip">💡 Tip: press <kbd>/</kbd> anywhere to jump to search.</div>
    <div class="modal-actions" style="margin-top:14px">
      <button type="button" class="btn btn-ghost" data-close-help>Close</button>
      <button type="button" class="btn btn-primary" data-open-demo>Book a Demo</button>
    </div>
  `);
  bindHelp('library-help');
}

// ---------- Help / modal infrastructure ----------
function injectHelpButton(label){
  if(document.querySelector('.help-fab')) return;
  const btn = document.createElement('button');
  btn.className = 'help-fab'; btn.type='button';
  btn.setAttribute('aria-label', label || 'Help');
  btn.setAttribute('data-open-help','');
  btn.textContent = '?';
  document.body.appendChild(btn);
}
function injectHelpModal(id, contentHtml){
  let host = document.getElementById(id); if(host) host.remove();
  host = document.createElement('div');
  host.className='modal-overlay'; host.id=id;
  host.setAttribute('role','dialog'); host.setAttribute('aria-modal','true');
  host.innerHTML = `<div class="modal help-modal">${contentHtml}</div>`;
  document.body.appendChild(host);
}
function openHelp(id){ const m = document.getElementById(id); if(!m) return; m.classList.add('open'); m.querySelector('button,a,input')?.focus(); }
function closeHelp(id){ document.getElementById(id)?.classList.remove('open'); }
function bindHelp(id){
  document.addEventListener('click', e=>{
    if(e.target.closest('[data-open-help]')){
      // route to the right help based on page context
      if(document.body.dataset.page==='detail') openHelp('walkthrough-modal');
      else openHelp(id);
    }
    if(e.target.closest('[data-close-help]')) closeHelp(id);
    if(e.target===document.getElementById(id)) closeHelp(id);
  });
  document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeHelp(id); });
}

// ---------- Demo modal ----------
function initModal(){
  const overlay = document.getElementById('demo-modal'); if(!overlay) return;
  function open(){ overlay.classList.add('open'); overlay.querySelector('input,button,select,textarea')?.focus(); }
  function close(){ overlay.classList.remove('open'); }
  document.addEventListener('click', e=>{
    if(e.target.closest('[data-open-demo]')){ e.preventDefault(); open(); }
    if(e.target.closest('[data-close-demo]')) close();
    if(e.target===overlay) close();
  });
  document.addEventListener('keydown', e=>{ if(e.key==='Escape') close(); });
  overlay.querySelector('form')?.addEventListener('submit', e=>{
    e.preventDefault();
    const f = e.target;
    f.innerHTML = `<h3>Thanks — we'll be in touch.</h3>
      <p class="muted">An Edstellar account manager will reach out within one business day to schedule your demo.</p>
      <div class="modal-actions"><button type="button" class="btn btn-primary" data-close-demo>Close</button></div>`;
  });
}

// ---------- FAQ & Tabs ----------
function initFAQ(){
  document.querySelectorAll('.faq-item').forEach(item=>{
    item.querySelector('.faq-q')?.addEventListener('click',()=>{
      const isOpen = item.hasAttribute('open');
      document.querySelectorAll('.faq-item[open]').forEach(o=>o.removeAttribute('open'));
      if(!isOpen) item.setAttribute('open','');
    });
  });
}
function initTabs(){
  document.querySelectorAll('.tabs').forEach(group=>{
    const btns = group.querySelectorAll('.tab-btn');
    btns.forEach(b=>b.addEventListener('click',()=>{
      const target = b.dataset.tab;
      btns.forEach(x=>x.classList.toggle('active', x===b));
      const scope = group.closest('[data-tab-scope]') || document;
      scope.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active', p.dataset.panel===target));
    }));
  });
}

// ---------- Landing: featured cards + rich category tiles ----------
async function initLandingFeatured(){
  const games = await loadGames();

  // Featured row
  const fhost = document.getElementById('featured-grid');
  if(fhost){
    const slugs = ['sales-jeopardy','escape-room','stress-free-bingo','leadership-pizza','empathy-mapping','egg-drop'];
    const picks = slugs.map(s => games.find(g=>g.slug===s)).filter(Boolean).slice(0,6);
    fhost.innerHTML = picks.map(gameCard).join('');
  }

  // Rich category tiles
  const rhost = document.getElementById('rich-cat-grid');
  if(rhost){
    const CATS = [
      ['Leadership',          'crown',     '#1E40AF', 'Coaching, alignment, conflict response, decision-making for managers.'],
      ['Communication',       'chat',      '#0F766E', 'Active listening, persuasion, nonverbal cues, message clarity.'],
      ['Sales',               'megaphone', '#F59E0B', 'Pitch drills, Jeopardy, objection handling, Shark Tank.'],
      ['Customer Service',    'heart',     '#0EA5E9', 'Empathy maps, complaint root-causing, tone-of-voice.'],
      ['Performance Management','chart',  '#0F766E', 'Feedback, KPI matchups, escape rooms, reverse mentoring.'],
      ['Change Management',   'shuffle',   '#7C3AED', 'Vision alignment, resistance sims, force-field analysis.'],
      ['Critical Thinking',   'brain',     '#A855F7', 'Murder mystery, logic puzzles, Socratic dialogue.'],
      ['Problem Solving',     'puzzle',    '#0EA5E9', 'Escape rooms, build challenges, scenario drills.'],
      ['Decision Making',     'compass',   '#9333EA', 'Trade-off games, dot voting, ethical dilemmas.'],
      ['Time Management',     'clock',     '#3B82F6', 'Pomodoro, Kanban, prioritization pyramid.'],
      ['Goal Setting',        'target',    '#DB2777', 'Vision boards, Work Bingo, AI goal coach.'],
      ['Accountability',      'handshake', '#16B8A6', 'Hot Seat, Trust Box, peer reviews, milestones.'],
      ['Stress / Wellness',   'leaf',      '#16A34A', 'Calm Jenga, breathing breaks, laughter therapy.'],
      ['HR / Onboarding',     'sparkle',   '#A855F7', 'Onboarding quests, values mapping, recognition.']
    ];
    const counts = {};
    games.forEach(g=>{ counts[g.category] = (counts[g.category]||0) + 1; });
    rhost.innerHTML = CATS.map(([cat,icon,accent,desc])=>{
      const n = counts[cat] || 0;
      const bg = catBg(cat);
      return `
      <a class="rich-cat-tile" href="./games.html?category=${encodeURIComponent(cat)}"
         style="--rc-bg:${bg};--rc-accent:${accent}">
        <div class="rich-cat-head">
          <span class="rich-cat-icon" style="background:${bg}">${svgIcon(icon,22).replace('class="card-icon"','')}</span>
          <h4>${escapeHtml(cat)}</h4>
          <span class="rich-cat-count">${n} games</span>
        </div>
        <p>${escapeHtml(desc)}</p>
        <span class="rich-cat-cta">View ${n} games →</span>
      </a>`;
    }).join('');
  }
}

// ---------- Library: spotlight ----------
async function initLibraryExtras(){
  const games = await loadGames();

  // Spotlight game — rotates daily based on date seed
  const spot = document.getElementById('spotlight-host');
  if(spot){
    const featured = games.filter(g => g.economy || (g.reinforcesTraining && (g.skills||[]).length > 0));
    const pool = featured.length ? featured : games;
    const dayIdx = Math.floor(Date.now() / (1000*60*60*24)) % pool.length;
    const pick = pool[dayIdx] || pool[0];
    if(pick){
      spot.innerHTML = `
        <a class="spotlight" href="./game.html?id=${encodeURIComponent(pick.slug)}" style="--sl-bg:${catBg(pick.category)};text-decoration:none;color:inherit">
          <span class="spotlight-mark">⭐ Spotlight</span>
          <span class="spotlight-icon" style="background:${catBg(pick.category)}">${svgIcon(catIcon(pick.category),32).replace('class="card-icon"','')}</span>
          <div class="spotlight-body">
            <h3>${escapeHtml(pick.title)}</h3>
            <p>${escapeHtml(pick.concept || pick.businessPurpose || '')}</p>
            <div class="spotlight-badges">
              <span class="badge badge-accent">${escapeHtml(pick.category)}</span>
              <span class="badge">${escapeHtml(pick.duration)}</span>
              <span class="badge">${escapeHtml(pick.format)}</span>
              ${pick.economy ? '<span class="badge badge-warn">🪙 Uses EngageCoins</span>' : ''}
              ${pick.reinforcesTraining ? '<span class="badge badge-warn">✓ Reinforces training</span>' : ''}
            </div>
          </div>
          <span class="btn btn-primary btn-sm">Open game →</span>
        </a>`;
    }
  }
}

// ---------- Game detail page ----------
async function initDetail(){
  const host = document.getElementById('detail-root'); if(!host) return;
  const games = await loadGames();
  const slug = new URLSearchParams(location.search).get('id');
  const game = games.find(g=>g.slug===slug) || games[0];
  if(!game){ host.innerHTML = '<p>Game not found.</p>'; return; }
  document.title = `${game.title} — Edstellar Engage`;

  const related = games.filter(g=>g.category===game.category && g.slug!==game.slug).slice(0,4);
  const howToFull = (game.howToPlay||[]).map((s,i)=>`<li ${i>=4?'class="collapsed-item"':''}>${escapeHtml(s)}</li>`).join('');
  const hasMoreSteps = (game.howToPlay||[]).length > 4;
  const variations = game.variations && game.variations.length ? game.variations : [];
  const variationsHtml = variations.length
    ? `<ul>${variations.map((v,i)=>`<li ${i>=3?'class="collapsed-item"':''}>${escapeHtml(v)}</li>`).join('')}</ul>${variations.length>3?'<button class="collapse-toggle" data-collapse-toggle>Show all variations</button>':''}`
    : `<p class="muted" style="margin:0">No variations published yet — check the source blog for ideas.</p>`;

  const skillsHtml = (game.skills||[]).length
    ? `<div class="skill-row">${game.skills.map(s=>`<span class="skill-pill">${escapeHtml(s)}</span>`).join('')}</div>` : '';

  const reinforceHtml = game.reinforcesTraining ? `
    <div class="reinforce">
      <small>Reinforces Edstellar training</small>
      <h4>${escapeHtml(game.trainingProgram || 'Edstellar Training')}</h4>
      <p>Run this game at 14 and 30 days post-training for best retention.</p>
      <a class="btn btn-accent btn-sm" href="${escapeHtml(game.trainingUrl||'#')}" target="_blank" rel="noopener">Bundle with training →</a>
    </div>` : '';

  // Currency CONCEPT (read-only, login-gated)
  const ecoHtml = game.economy ? renderCurrencyConcept(game) : '';

  // TOC anchors
  const tocItems = [
    ['concept','Concept'],
    ['outcomes','Business outcomes'],
    ['how-to','How to play'],
    ['needs','What you need'],
    ['variations','Variations'],
    ['review','Review questions'],
    ['takeaway','Key takeaway'],
    game.economy ? ['currency','EngageCoins'] : null,
    ['related','Related games']
  ].filter(Boolean);

  host.innerHTML = `
    <div class="detail-shell">
      <div class="crumbs"><a href="./games.html">Games</a> / <a href="./games.html?category=${encodeURIComponent(game.category)}">${escapeHtml(game.category)}</a> / ${escapeHtml(game.title)}</div>

      <div class="detail-hero">
        <div>
          <span class="eyebrow">${escapeHtml(game.type || 'Workplace activity')}</span>
          <h1 class="detail-title">${escapeHtml(game.title)}</h1>
          <p class="lead">${escapeHtml(game.concept || '')}</p>
          ${skillsHtml}
          <div class="detail-stats">
            <div class="detail-stat"><small>Duration</small><strong>${escapeHtml(game.duration)}</strong></div>
            <div class="detail-stat"><small>Team</small><strong>${escapeHtml(game.team)}</strong></div>
            <div class="detail-stat"><small>Format</small><strong>${escapeHtml(game.format)}</strong></div>
            <div class="detail-stat"><small>Difficulty</small><strong>${escapeHtml(game.difficulty)}</strong></div>
            <div class="detail-stat"><small>Facilitator</small><strong>${escapeHtml(game.facilitator||'None')}</strong></div>
          </div>
          <div class="hero-cta" style="margin-top:18px">
            <button class="btn btn-primary btn-lg" data-open-demo>Run this game with your team</button>
            <a class="btn btn-ghost btn-lg" href="./games.html">Back to library</a>
          </div>
        </div>
        <div class="detail-hero-art" style="background:${catBg(game.category)}">${svgIcon(catIcon(game.category),88)}</div>
      </div>

      <div class="detail-body">
        <div>
          <section class="panel section-anchor" id="concept">
            <h2>Concept</h2>
            <p>${escapeHtml(game.concept || game.businessPurpose || '')}</p>
            ${game.businessPurpose ? `<p class="muted"><strong style="color:var(--brand-primary)">Business purpose:</strong> ${escapeHtml(game.businessPurpose)}</p>` : ''}
          </section>

          <section class="panel section-anchor" id="outcomes">
            <h2>Business outcomes</h2>
            <ul>${(game.outcomes||[game.businessPurpose].filter(Boolean)).map(o=>`<li>${escapeHtml(o)}</li>`).join('')}</ul>
          </section>

          <section class="panel section-anchor" id="how-to">
            <h2>How to play</h2>
            <ol class="collapsible">${howToFull}</ol>
            ${hasMoreSteps ? `<button class="collapse-toggle" data-collapse-toggle>Show all ${game.howToPlay.length} steps</button>` : ''}
          </section>

          <section class="panel section-anchor" id="needs">
            <h2>What you need</h2>
            <p><strong style="color:var(--brand-primary)">Materials:</strong> ${escapeHtml(game.materials || game.needs?.materials || 'Browser. Optional printables.')}</p>
            <p><strong style="color:var(--brand-primary)">Platform features:</strong> ${escapeHtml(game.needs?.platform || 'Engage facilitator console, timer, team rooms, leaderboard.')}</p>
            <p><strong style="color:var(--brand-primary)">Facilitator:</strong> ${escapeHtml(game.needs?.facilitator || game.facilitator || 'Optional.')}</p>
          </section>

          <section class="panel section-anchor" id="variations">
            <h2>Variations</h2>
            <div class="collapsible">${variationsHtml}</div>
          </section>

          <section class="panel section-anchor" id="review">
            <h2>Review questions for the debrief</h2>
            <p class="muted">Run these questions after the game to lock in the learning.</p>
            <ol>${(game.reviewQuestions||[]).map(q=>`<li>${escapeHtml(q)}</li>`).join('') || '<li>What did you learn from this activity?</li>'}</ol>
          </section>

          <section class="panel section-anchor" id="takeaway">
            <h2>Key takeaway</h2>
            <p>${escapeHtml(game.keyTakeaway || 'The value comes from the debrief — connect what happened in the game to what changes at work.')}</p>
          </section>

          ${game.economy ? `<section class="panel section-anchor" id="currency" style="padding:0;background:transparent;border:none">${ecoHtml}</section>` : ''}

          <section class="panel section-anchor" id="related">
            <h2>Related games</h2>
            <div class="cards-grid">
              ${related.length ? related.map(gameCard).join('') : '<p class="muted">No related games yet.</p>'}
            </div>
            <p class="muted" style="margin-top:12px;font-size:13px">Source: <a href="${escapeHtml(game.sourceBlog||'#')}" target="_blank" rel="noopener">${escapeHtml(game.sourceBlogTitle||'Edstellar blog')}</a></p>
          </section>
        </div>

        <aside class="aside">
          <div class="toc" aria-label="On this page">
            <h4>On this page</h4>
            <ul>${tocItems.map(([id,label])=>`<li><a href="#${id}" data-toc="${id}">${escapeHtml(label)}</a></li>`).join('')}</ul>
          </div>
          ${reinforceHtml}
        </aside>
      </div>
    </div>`;

  // Collapsibles
  host.querySelectorAll('[data-collapse-toggle]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const parent = btn.previousElementSibling?.classList.contains('collapsible')
        ? btn.previousElementSibling
        : btn.parentElement.querySelector('.collapsible');
      if(!parent) return;
      const isOpen = parent.classList.toggle('open');
      btn.textContent = isOpen ? 'Show fewer' : btn.textContent.replace('Show fewer', 'Show all');
    });
  });

  // TOC scroll-spy
  const links = host.querySelectorAll('.toc a[data-toc]');
  const targets = Array.from(host.querySelectorAll('.section-anchor'));
  function highlight(){
    const y = window.scrollY + 120;
    let current = targets[0]?.id;
    for(const t of targets){ if(t.offsetTop <= y) current = t.id; }
    links.forEach(a=>a.classList.toggle('active', a.dataset.toc===current));
  }
  highlight(); window.addEventListener('scroll', highlight, {passive:true});

  // Walkthrough — auto-open on first visit
  initWalkthrough(game);
}

// ---------- Currency CONCEPT (read-only, login-gated) ----------
function renderCurrencyConcept(game){
  const eco = game.economy;
  const items = (eco.shop||[]).map(item => `
    <div class="eco-item">
      <div class="eco-item-head">
        <span class="eco-item-name"><span class="ico">${escapeHtml(item.icon||'•')}</span>${escapeHtml(item.name)}</span>
        <span class="eco-item-cost"><span class="coin">¢</span>${item.cost}</span>
      </div>
      <p>${escapeHtml(item.effect)}</p>
      <span class="eco-lock">🔒 Available in-game</span>
    </div>`).join('');
  const explainer = eco.explainer || 'EngageCoins are an in-game budget. Spend them on power-ups or items to change how a round plays out.';
  return `
    <div class="eco-concept">
      <div class="eco-head">
        <span class="eco-coin">¢</span>
        <h3>This game uses ${escapeHtml(eco.currency || 'EngageCoins')}</h3>
        <span class="eco-tag">Concept</span>
      </div>
      <p class="eco-body">${escapeHtml(explainer)}</p>
      <div class="eco-meta">
        <span class="eco-balance"><span class="coin" style="width:14px;height:14px;border-radius:50%;background:linear-gradient(135deg,#FCD34D,#F59E0B);display:inline-flex"></span>Players start with ${eco.starting} ${escapeHtml(eco.currency||'coins')}</span>
      </div>
      <div class="eco-section-label">Ways to earn coins</div>
      <ul class="eco-rules">${(eco.earnRules||[]).map(r=>`<li>${escapeHtml(r)}</li>`).join('')}</ul>
      <div class="eco-section-label">Shop preview</div>
      <div class="eco-shop">${items}</div>
      <div class="eco-cta">
        <button class="btn btn-accent" data-open-demo>Sign in to start playing</button>
        <p class="eco-cta-note">The shop, your balance, and persistent purchases are available once you sign in and join an active game session. This preview is a read-only concept overview.</p>
      </div>
    </div>`;
}

// ---------- Walkthrough (4 steps from structured fields) ----------
function initWalkthrough(game){
  const stepIcons = ['lightbulb','play','chatbox','star'];
  const fallback = [
    {title:`What is ${game.title}?`, body: game.concept || game.businessPurpose || 'A workplace activity from the Edstellar library.'},
    {title:'How a round plays out', body:(game.howToPlay||[]).slice(0,3).map((s,i)=>`Step ${i+1}: ${s}`).join(' ') || 'A facilitator guides the team through the activity step by step.'},
    {title:`Questions you'll discuss after`, body:(game.reviewQuestions||[]).slice(0,3).map(q=>'• '+q).join(' ') || '• What worked? • What didn\'t? • How will you apply this at work?'},
    {title:'Why this game matters', body: game.keyTakeaway || game.businessPurpose || 'Every Engage game ties to real behavior change at work.'}
  ];
  const steps = (game.walkthrough && game.walkthrough.length===4) ? game.walkthrough : fallback;
  let idx = 0;

  injectHelpButton(`How to play ${game.title}`);
  injectHelpModal('walkthrough-modal', `<div class="walkthrough" id="walk-body"></div>`);
  bindHelp('walkthrough-modal');

  const render = () => {
    const isLast = idx === steps.length - 1;
    const dots = steps.map((_,i)=>`<span class="${i<idx?'done':i===idx?'active':''}"></span>`).join('');
    document.getElementById('walk-body').innerHTML = `
      <div class="walk-icon">${svgIcon(stepIcons[idx]||'star',36).replace('class="card-icon"','')}</div>
      <div class="walk-progress" aria-hidden="true">${dots}</div>
      <div class="walk-content walk-slide">
        <h3>${escapeHtml(steps[idx].title)}</h3>
        <p class="body">${escapeHtml(steps[idx].body)}</p>
      </div>
      <div class="walk-actions">
        <button type="button" class="walk-skip" data-walk-skip>${isLast?'Got it':'Skip walkthrough'}</button>
        <div style="display:flex;gap:8px">
          ${idx>0?'<button type="button" class="btn btn-ghost btn-sm" data-walk-prev>Back</button>':''}
          <button type="button" class="btn btn-primary btn-sm" data-walk-next>${isLast?'Start playing':'Next →'}</button>
        </div>
      </div>
      <div class="walk-foot">
        <label><input type="checkbox" id="walk-skip-all" ${localStorage.getItem('engage-walk-skip-all')==='1'?'checked':''}/> Don't show again for any game</label>
        <span>Step ${idx+1} of ${steps.length}</span>
      </div>`;
    document.getElementById('walk-skip-all')?.addEventListener('change', e=>{
      localStorage.setItem('engage-walk-skip-all', e.target.checked ? '1' : '0');
    });
  };
  render();

  document.getElementById('walkthrough-modal').addEventListener('click', e=>{
    if(e.target.closest('[data-walk-next]')){
      if(idx < steps.length - 1){ idx++; render(); }
      else closeHelp('walkthrough-modal');
    } else if(e.target.closest('[data-walk-prev]')){
      if(idx>0){ idx--; render(); }
    } else if(e.target.closest('[data-walk-skip]')){
      closeHelp('walkthrough-modal');
    }
  });

  // Auto-open on first visit unless suppressed
  const seenKey = `engage-walk-seen-${game.slug}`;
  const skipAll = localStorage.getItem('engage-walk-skip-all')==='1';
  if(!localStorage.getItem(seenKey) && !skipAll){
    setTimeout(()=>{ openHelp('walkthrough-modal'); localStorage.setItem(seenKey,'1'); }, 380);
  }
}

// ---------- Boot ----------
document.addEventListener('DOMContentLoaded', ()=>{
  initModal(); initFAQ(); initTabs();
  if(document.body.dataset.page==='landing') initLandingFeatured();
  if(document.body.dataset.page==='library'){ initLibrary(); initLibraryHelp(); initLibraryExtras(); }
  if(document.body.dataset.page==='detail') initDetail();
});
