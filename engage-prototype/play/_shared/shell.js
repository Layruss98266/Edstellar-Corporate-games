/* ===========================================================
   Edstellar Engage - Shared Game Shell (JS)
   Pure utilities. No game state. Every utility either takes
   its inputs as parameters or reads DOM elements by their
   standardised IDs (toast, ariaAnnouncer, confetti, modeBanner,
   hcToggle, streakPill, streakDays, undoBanner, undoText).
=========================================================== */
(function(global){
  'use strict';

  const Shell = {};

  /* ---------- Tiny DOM helpers ---------- */
  Shell.$ = id => document.getElementById(id);
  Shell.makeId = () => crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random());
  Shell.safe = v => String(v ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}[c]));

  /* ---------- Toast ---------- */
  Shell.toast = function(msg, kind=''){
    const t = Shell.$('toast'); if(!t) return;
    t.textContent = msg;
    t.className = 'toast show ' + kind;
    clearTimeout(Shell.toast._t);
    Shell.toast._t = setTimeout(() => t.classList.remove('show'), 1700);
  };

  /* ---------- ARIA announcer ---------- */
  Shell.announce = function(msg){
    const el = Shell.$('ariaAnnouncer'); if(!el) return;
    el.textContent = '';
    setTimeout(() => el.textContent = msg, 50);
  };

  /* ---------- Confetti (canvas, brand colors) ---------- */
  Shell.fireConfetti = function(){
    const c = Shell.$('confetti'); if(!c) return;
    const ctx = c.getContext('2d');
    c.width = window.innerWidth; c.height = window.innerHeight;
    const colors = ['#0B3C5D','#2563EB','#10B981','#F59E0B','#7C3AED','#EC4899','#38BDF8'];
    const parts = Array.from({length:120}, () => ({
      x: c.width/2 + (Math.random()-.5)*120, y: c.height/2 + (Math.random()-.5)*60,
      vx:(Math.random()-.5)*14, vy:-Math.random()*14-4,
      g:.35+Math.random()*.2, s:4+Math.random()*6,
      r:Math.random()*Math.PI, vr:(Math.random()-.5)*.3,
      color: colors[Math.floor(Math.random()*colors.length)],
      life:80+Math.random()*60
    }));
    function tick(){
      ctx.clearRect(0,0,c.width,c.height);
      let alive = false;
      parts.forEach(p => {
        if(p.life-- <= 0) return;
        alive = true;
        p.x += p.vx; p.y += p.vy; p.vy += p.g; p.r += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r);
        ctx.fillStyle = p.color; ctx.fillRect(-p.s/2,-p.s/2, p.s, p.s*1.4);
        ctx.restore();
      });
      if(alive) requestAnimationFrame(tick); else ctx.clearRect(0,0,c.width,c.height);
    }
    tick();
  };
  window.addEventListener('resize', () => { const c = Shell.$('confetti'); if(c){ c.width=window.innerWidth; c.height=window.innerHeight; }});

  /* ---------- Beep ---------- */
  Shell.beep = function(freq=760, ms=220){
    try{
      const a = new (window.AudioContext||window.webkitAudioContext)();
      const o = a.createOscillator(); const g = a.createGain();
      o.connect(g); g.connect(a.destination);
      o.frequency.value = freq;
      g.gain.setValueAtTime(.08, a.currentTime);
      g.gain.exponentialRampToValueAtTime(.001, a.currentTime + ms/1000);
      o.start(); setTimeout(() => { o.stop(); a.close(); }, ms);
    } catch(e){}
  };

  /* ---------- Fullscreen ---------- */
  Shell.fullscreen = async function(){
    try{
      if(!document.fullscreenElement && document.documentElement.requestFullscreen)
        await document.documentElement.requestFullscreen();
    } catch(e){}
  };

  /* ---------- File download ---------- */
  Shell.download = function(filename, content, mime='application/json'){
    const blob = new Blob([content], {type: mime});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  };

  /* ---------- 14-day .ics reminder ---------- */
  Shell.downloadIcs = function(opts){
    const o = Object.assign({days:14, summary:'Edstellar Engage - Reinforcement Session', description:'Replay with the same teams. Beat the forgetting curve.', filename:'engage-reminder.ics'}, opts||{});
    const start = new Date(Date.now() + o.days*24*60*60*1000); start.setHours(10,0,0,0);
    const end = new Date(start.getTime() + 30*60*1000);
    const fmt = d => d.toISOString().replace(/[-:]/g,'').replace(/\.\d{3}/, '');
    const ics = ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Edstellar Engage//Game//EN','BEGIN:VEVENT',
      'UID:'+Shell.makeId()+'@edstellar.com','DTSTAMP:'+fmt(new Date()),'DTSTART:'+fmt(start),'DTEND:'+fmt(end),
      'SUMMARY:'+o.summary,'DESCRIPTION:'+o.description,'END:VEVENT','END:VCALENDAR'].join('\r\n');
    Shell.download(o.filename, ics, 'text/calendar');
    Shell.toast('Reminder downloaded', 'success');
  };

  /* ---------- Clipboard ---------- */
  Shell.copy = function(text){
    if(navigator.clipboard) navigator.clipboard.writeText(text).then(
      () => Shell.toast('Copied!', 'success'),
      () => Shell.toast('Copy failed', 'warning')
    );
    else Shell.toast('Clipboard unavailable', 'warning');
  };

  /* ---------- Share state (hash-based, no backend) ----------
     state: any JSON-serialisable object. Sensitive fields (hidden
     answers, lie markers) should be stripped by the caller. */
  Shell.buildShareLink = function(state){
    const enc = btoa(unescape(encodeURIComponent(JSON.stringify(state))));
    return location.origin + location.pathname + '#s=' + enc;
  };
  Shell.loadFromHash = function(){
    if(!location.hash.startsWith('#s=')) return null;
    try{
      return JSON.parse(decodeURIComponent(escape(atob(location.hash.slice(3)))));
    } catch(e){ return null; }
  };
  Shell.buildEmbed = function(){
    return `<iframe src="${location.origin}${location.pathname}?mode=present" width="600" height="800" frameborder="0" allow="fullscreen"></iframe>`;
  };

  /* ---------- Modes (URL param driven) ---------- */
  Shell.detectMode = function(){
    const m = new URLSearchParams(location.search).get('mode');
    const banner = Shell.$('modeBanner');
    if(m === 'present'){ document.body.classList.add('mode-present'); if(banner) banner.innerHTML = '📺 Presenter mode · <a href="?">exit</a>'; }
    else if(m === 'play'){ document.body.classList.add('mode-play'); if(banner) banner.innerHTML = '📱 Player mode · <a href="?">exit</a>'; }
  };

  /* ---------- Daily streak tracker ----------
     keys: { last: 'edstellarFooLastSession', streak: 'edstellarFooStreak' } */
  Shell.updateStreak = function(keys){
    const last = Number(localStorage.getItem(keys.last) || 0);
    let streak = Number(localStorage.getItem(keys.streak) || 0);
    const today = new Date(); today.setHours(0,0,0,0);
    if(last){
      const lastDay = new Date(last); lastDay.setHours(0,0,0,0);
      const days = Math.floor((today - lastDay) / (1000*60*60*24));
      if(days === 0){} else if(days === 1) streak += 1; else streak = 1;
    } else streak = 1;
    localStorage.setItem(keys.streak, String(streak));
    localStorage.setItem(keys.last, String(Date.now()));
    const pill = Shell.$('streakPill'); const days = Shell.$('streakDays');
    if(streak >= 2 && pill){ pill.style.display = 'inline-flex'; if(days) days.textContent = streak; }
    return streak;
  };

  /* ---------- Language (RTL on Arabic) ---------- */
  Shell.setLanguage = function(lang){
    document.documentElement.lang = lang;
    document.body.dir = lang === 'ar' ? 'rtl' : 'ltr';
    const sel = Shell.$('langSelect'); if(sel) sel.value = lang;
  };

  /* ---------- High-contrast toggle ---------- */
  Shell.applyHc = function(on, storageKey){
    document.body.classList.toggle('hc', !!on);
    const t = Shell.$('hcToggle'); if(t) t.checked = !!on;
    if(storageKey) localStorage.setItem(storageKey, on ? '1' : '0');
  };

  /* ---------- Phase setter (drives §7 status gradient + §5 stepper) ---------- */
  Shell.setPhase = function(p, allPhases){
    (allPhases || ['setup','build','prompt','perform','event','drop','submit','vote','reveal','review','score'])
      .forEach(x => { const el = Shell.$('flow-'+x); if(el) el.classList.toggle('active', x === p); });
    document.body.dataset.phase = p;
    const ps = Shell.$('phaseStat'); if(ps) ps.textContent = p[0].toUpperCase() + p.slice(1);
  };

  /* ---------- Timer (with warn/danger pulse + status-progress bar) ---------- */
  Shell.startTimer = function(seconds, opts){
    const o = Object.assign({onTick:null, onEnd:null, warnAt:30, dangerAt:10}, opts||{});
    let remaining = seconds;
    Shell.stopTimer();
    const tick = () => {
      const m = String(Math.floor(Math.max(0, remaining)/60)).padStart(2,'0');
      const s = String(Math.max(0, remaining)%60).padStart(2,'0');
      const t = Shell.$('timer'); if(t){ t.textContent = `⏱ ${m}:${s}`;
        t.classList.toggle('warn', remaining <= o.warnAt && remaining > o.dangerAt);
        t.classList.toggle('danger', remaining <= o.dangerAt && remaining > 0);
      }
      const fill = Shell.$('statusProgressFill');
      if(fill) fill.style.width = Math.max(0, Math.min(100, (remaining/seconds)*100)) + '%';
      if(o.onTick) o.onTick(remaining);
    };
    tick();
    Shell._timer = setInterval(() => {
      remaining--;
      tick();
      if(remaining <= 0){ Shell.stopTimer(); if(o.onEnd) o.onEnd(); }
    }, 1000);
    return () => Shell.stopTimer();
  };
  Shell.stopTimer = function(){ if(Shell._timer){ clearInterval(Shell._timer); Shell._timer = null; } };

  /* ---------- Undo banner ---------- */
  Shell.showUndoBanner = function(msg, ms=12000){
    const b = Shell.$('undoBanner'); const t = Shell.$('undoText');
    if(!b) return;
    if(t) t.textContent = msg;
    b.classList.add('show');
    clearTimeout(Shell.showUndoBanner._t);
    Shell.showUndoBanner._t = setTimeout(() => b.classList.remove('show'), ms);
  };
  Shell.hideUndoBanner = function(){ const b = Shell.$('undoBanner'); if(b) b.classList.remove('show'); };

  /* ---------- View switching with optional gated views ----------
     gated: array of view names that require a confirm before showing.
     onGate(view, allow): called when a gated view is clicked.
     locks: object tracking which gated views are currently unlocked. */
  Shell.makeViewSwitcher = function(views, opts){
    const o = Object.assign({gated:[], onGate:null}, opts||{});
    const locks = {};
    function switchView(v){
      if(o.gated.includes(v) && !locks[v]){
        if(o.onGate){ o.onGate(v, () => { locks[v] = true; switchView(v); }); return; }
      }
      views.forEach(x => { const el = Shell.$(x+'View'); if(el) el.classList.toggle('hidden', x !== v); });
      document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.view === v));
      // Auto-lock all gated views you're not currently on
      o.gated.forEach(g => { if(g !== v) locks[g] = false; });
      if(opts && opts.onSwitch) opts.onSwitch(v);
    }
    return { switchView, locks };
  };

  /* ---------- Brand palette (teams) ---------- */
  Shell.TEAM_COLORS = ['#0B3C5D','#2563EB','#10B981','#F59E0B','#7C3AED','#EC4899','#0EA5E9','#F97316'];
  Shell.TEAM_AVATARS = ['🦅','⚡','🔥','🌟','🚀','🛡','🎯','🦄'];

  /* ---------- 14-language dropdown options (HTML) ---------- */
  Shell.LANGUAGE_OPTIONS = [
    ['en','English'],['hi','हिन्दी · Hindi'],['ar','العربية · Arabic (RTL)'],
    ['es','Español · Spanish'],['fr','Français · French'],['de','Deutsch · German'],
    ['pt','Português · Portuguese'],['ja','日本語 · Japanese'],['ko','한국어 · Korean'],
    ['zh','中文 · Chinese'],['ru','Русский · Russian'],['it','Italiano · Italian'],
    ['id','Bahasa Indonesia'],['tr','Türkçe · Turkish']
  ];
  Shell.languageOptionsHtml = function(selected='en'){
    return Shell.LANGUAGE_OPTIONS.map(([v,l]) => `<option value="${v}" ${v===selected?'selected':''}>${l}</option>`).join('');
  };

  /* ---------- Confirm-and-reset helper ---------- */
  Shell.confirmReset = function(opts){
    const o = Object.assign({message:'Reset all game state? This clears teams, rounds, and saved progress.', storageKey:null, onReset:null}, opts||{});
    if(!confirm(o.message)) return false;
    if(o.storageKey) localStorage.removeItem(o.storageKey);
    if(o.onReset) o.onReset();
    Shell.toast('Game reset', 'success');
    Shell.announce('Game reset.');
    return true;
  };

  /* ---------- CSV export ---------- */
  Shell.exportCsv = function(filename, rows){
    const csv = rows.map(r => r.map(c => `"${String(c ?? '').replace(/"/g,'""')}"`).join(',')).join('\n');
    Shell.download(filename, csv, 'text/csv');
    Shell.toast('CSV exported', 'success');
  };

  /* ---------- Autosave label refresh ---------- */
  Shell.bindAutosaveLabel = function(getLastSaveAt){
    const update = () => {
      const el = Shell.$('autosaveLabel'); if(!el) return;
      const last = getLastSaveAt(); if(!last){ el.textContent = 'Not saved yet'; return; }
      const diff = Math.floor((Date.now() - last) / 1000);
      el.textContent = diff < 5 ? 'Saved just now' : diff < 60 ? `Saved ${diff}s ago` : `Saved ${Math.floor(diff/60)}m ago`;
    };
    update();
    setInterval(update, 5000);
  };

  /* ---------- Global keyboard binder ----------
     Pass a map { key: handler } where key is the lowercased character
     or 'space'/'escape'/'?'. Inputs/textareas/selects are skipped. */
  Shell.bindKeys = function(map){
    document.addEventListener('keydown', e => {
      if(e.target.matches('input,textarea,select')) return;
      const key = e.key === ' ' ? 'space' : e.key === 'Escape' ? 'escape' : e.key.toLowerCase();
      const h = map[key] || (key === '/' && e.shiftKey ? map['?'] : null);
      if(h){ e.preventDefault(); h(e); }
    });
  };

  global.EngageShell = Shell;
  global.$ = Shell.$;
})(window);
