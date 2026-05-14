"""
Generate the marketing pages for Edstellar Engage:
- pricing.html
- use-cases.html
- how-it-works.html
- facilitated.html
- compare.html
- case-studies.html
- about.html

Run from repo root or this folder:
  python engage-prototype/_build/build_pages.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent  # engage-prototype/

NAV_LINKS = [
    ('./games.html', 'Games'),
    ('./how-it-works.html', 'How it works'),
    ('./use-cases.html', 'Use Cases'),
    ('./pricing.html', 'Pricing'),
    ('./compare.html', 'Compare'),
]

FOOTER_PRODUCT = [
    ('./games.html', 'Game Library'),
    ('./how-it-works.html', 'How it works'),
    ('./use-cases.html', 'Use Cases'),
    ('./pricing.html', 'Pricing'),
    ('./compare.html', 'Compare'),
    ('./facilitated.html', 'Facilitated Sessions'),
]
FOOTER_SOLUTIONS = [
    ('./games.html?category=Sales', 'Sales Enablement'),
    ('./games.html?category=Customer%20Service', 'Customer Service'),
    ('./games.html?category=Leadership', 'Leadership'),
    ('./games.html?category=HR%20%2F%20Onboarding', 'HR & Onboarding'),
]
FOOTER_RESOURCES = [
    ('./case-studies.html', 'Case studies'),
    ('./facilitated.html', 'Facilitator program'),
    ('./games.html', 'Game Library'),
]
FOOTER_COMPANY = [
    ('./about.html', 'About Engage'),
    ('https://www.edstellar.com', 'Edstellar.com'),
    ('#', 'Contact'),
    ('#', 'Privacy'),
]

def nav(active=''):
    links = ''.join(
        f'<a href="{href}"{" class=\"active\"" if active==href else ""}>{label}</a>'
        for href, label in NAV_LINKS
    )
    return f'''<header class="nav">
  <div class="container nav-inner">
    <a class="brand" href="./index.html">
      <span class="brand-logo" aria-hidden="true"></span>
      <span>Edstellar <span style="color:var(--brand-accent-700)">Engage</span></span>
    </a>
    <nav class="nav-links" aria-label="Primary">{links}</nav>
    <div class="nav-cta">
      <a class="btn btn-ghost btn-sm" href="#">Sign in</a>
      <button class="btn btn-primary btn-sm" data-open-demo>Book a Demo</button>
    </div>
  </div>
</header>'''

def footer_col(title, links):
    items = ''.join(f'<li><a href="{h}">{l}</a></li>' for h, l in links)
    return f'<div><h5>{title}</h5><ul>{items}</ul></div>'

def footer():
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="./index.html" style="color:#fff">
          <span class="brand-logo"></span>
          <span style="color:#fff">Edstellar <span style="color:var(--brand-accent)">Engage</span></span>
        </a>
        <p style="margin-top:12px;color:#94A3B8;font-size:14px;max-width:280px">Interactive workplace games for engagement, reinforcement, and culture. Part of the Edstellar talent transformation suite.</p>
      </div>
      {footer_col('Product', FOOTER_PRODUCT)}
      {footer_col('Solutions', FOOTER_SOLUTIONS)}
      {footer_col('Resources', FOOTER_RESOURCES)}
      {footer_col('Company', FOOTER_COMPANY)}
    </div>
    <div class="footer-legal"><span>© 2026 Edstellar. All rights reserved.</span><span>engage.edstellar.com</span></div>
  </div>
</footer>'''

DEMO_MODAL = '''<div class="modal-overlay" id="demo-modal" role="dialog" aria-modal="true" aria-labelledby="demo-modal-title">
  <div class="modal">
    <form class="modal-form" novalidate>
      <h3 id="demo-modal-title">Book a 20-minute demo</h3>
      <p class="muted">Tell us about your team. We'll preload a workspace with your branding for the call.</p>
      <label>Work email<input type="email" required placeholder="you@company.com"/></label>
      <label>Company<input type="text" required placeholder="Company name"/></label>
      <label>Team size<select required><option value="">Select...</option><option>1-50</option><option>50-200</option><option>200-1,000</option><option>1,000+</option></select></label>
      <label>What are you trying to solve?<textarea rows="3" placeholder="e.g., post-training reinforcement for our sales team"></textarea></label>
      <div class="modal-actions">
        <button type="button" class="btn btn-ghost" data-close-demo>Cancel</button>
        <button type="submit" class="btn btn-primary">Request demo</button>
      </div>
    </form>
  </div>
</div>'''

def page(filename, title, body_html, active_nav='', page_attr='marketing'):
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<link rel="stylesheet" href="./assets/styles.css"/>
</head>
<body data-page="{page_attr}">
{nav(active_nav)}
{body_html}
{footer()}
<button class="btn btn-accent sticky-cta" data-open-demo>Book a Demo</button>
{DEMO_MODAL}
<script src="./assets/games-data.js"></script>
<script src="https://cdn.jsdelivr.net/npm/motion@10.18.0/dist/motion.min.js" defer></script>
<script src="./assets/app.js"></script>
<script src="./assets/motion.js" defer></script>
</body>
</html>'''
    (OUT / filename).write_text(html, encoding='utf-8')
    print(f'Wrote {filename}')

# ---------------- PRICING ----------------
PRICING_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">Pricing</span>
    <h1>Engagement built for HR and L&amp;D budgets.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">Per-employee plans, plus facilitated event tiers. Existing Edstellar training clients get Engage as a 15-20% add-on - no separate procurement.</p>
    <div class="hero-cta" style="justify-content:center"><button class="btn btn-primary btn-lg" data-open-demo>Book a Demo</button><a class="btn btn-ghost btn-lg" href="#plans">See plans</a></div>
  </div>
</section>

<section class="section" id="plans" style="padding-top:8px">
  <div class="container">
    <div class="price-grid">
      <div class="price-card">
        <h3>Team</h3>
        <div class="price-amount">$3<small> /employee /mo</small></div>
        <p class="muted">50-200 employees</p>
        <ul class="price-feat">
          <li>Full game library (200+ games)</li>
          <li>Custom branding</li>
          <li>Monthly engagement reports</li>
          <li>Email support</li>
          <li>14-day free trial</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Start Trial</button>
      </div>
      <div class="price-card popular">
        <span class="price-ribbon">MOST POPULAR</span>
        <h3>Business</h3>
        <div class="price-amount">$2<small> /employee /mo</small></div>
        <p class="muted">200-1,000 employees</p>
        <ul class="price-feat">
          <li>Everything in Team</li>
          <li>SSO (Okta, Azure AD, Google)</li>
          <li>Advanced analytics + exports</li>
          <li>API access</li>
          <li>Priority support</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Book a Demo</button>
      </div>
      <div class="price-card">
        <h3>Enterprise</h3>
        <div class="price-amount">From $1.25<small> /employee /mo</small></div>
        <p class="muted">1,000+ employees · $25K floor</p>
        <ul class="price-feat">
          <li>Everything in Business</li>
          <li>HRIS sync (Workday, BambooHR)</li>
          <li>SCORM/xAPI for LMS</li>
          <li>Dedicated CSM + SLAs</li>
          <li>Regional data residency</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Talk to Sales</button>
      </div>
      <div class="price-card">
        <h3>Facilitated</h3>
        <div class="price-amount">From $1,500<small> /event</small></div>
        <p class="muted">Hosted live events, any team size</p>
        <ul class="price-feat">
          <li>Edstellar facilitator included</li>
          <li>Custom game design</li>
          <li>Post-session debrief report</li>
          <li>Hybrid, virtual, or in-person</li>
          <li>Available in India, MEA, APAC</li>
        </ul>
        <a class="btn btn-primary" href="./facilitated.html">Explore Facilitated →</a>
      </div>
    </div>
    <p class="muted" style="margin-top:24px;text-align:center;font-size:13.5px">Existing Edstellar training clients: Engage attaches as a <strong style="color:var(--brand-primary)">15-20% add-on</strong> on the training contract - talk to your account manager.</p>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border);border-bottom:1px solid var(--brand-border)">
  <div class="container">
    <h2>Plan comparison</h2>
    <p class="lead">Every feature that matters for HR, L&amp;D, IT, and procurement.</p>
    <div class="compare" style="margin-top:24px">
      <table>
        <thead><tr><th>Feature</th><th>Team</th><th class="col-engage">Business</th><th>Enterprise</th></tr></thead>
        <tbody>
          <tr><td>Game library (200+ games)</td><td class="check">✓</td><td class="col-engage check">✓</td><td class="check">✓</td></tr>
          <tr><td>Custom branding</td><td class="check">✓</td><td class="col-engage check">✓</td><td class="check">✓</td></tr>
          <tr><td>Engagement reports</td><td>Monthly</td><td class="col-engage">Advanced + exports</td><td>Custom dashboards</td></tr>
          <tr><td>SSO</td><td class="cross">-</td><td class="col-engage check">✓</td><td class="check">✓</td></tr>
          <tr><td>API access</td><td class="cross">-</td><td class="col-engage check">✓</td><td class="check">✓</td></tr>
          <tr><td>HRIS sync</td><td class="cross">-</td><td class="cross">-</td><td class="check">✓</td></tr>
          <tr><td>LMS interop (SCORM/xAPI)</td><td class="cross">-</td><td class="cross">-</td><td class="check">✓</td></tr>
          <tr><td>Data residency</td><td class="cross">-</td><td class="cross">-</td><td class="check">✓</td></tr>
          <tr><td>Dedicated CSM</td><td class="cross">-</td><td class="cross">-</td><td class="check">✓</td></tr>
          <tr><td>SLA</td><td class="cross">-</td><td class="cross">-</td><td class="check">99.9%</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:820px">
    <h2>Pricing FAQ</h2>
    <div style="margin-top:18px">
      <div class="faq-item"><button class="faq-q">Is there a free trial?</button><div class="faq-a">Yes - 14 days on the Team plan, no card required. Up to 25 employees, full game library, monthly report.</div></div>
      <div class="faq-item"><button class="faq-q">Are there annual discounts?</button><div class="faq-a">Annual billing saves ~15% on Team and Business plans. Enterprise contracts are negotiated per-deal with multi-year discount tiers.</div></div>
      <div class="faq-item"><button class="faq-q">What counts as an employee?</button><div class="faq-a">Anyone who can join a game room or receive a campaign. You pay for active employees in the period - not headcount on paper. Inactive users don't count toward your plan.</div></div>
      <div class="faq-item"><button class="faq-q">Can we mix Engage with the Facilitated tier?</button><div class="faq-a">Yes. Most Business and Enterprise clients run the SaaS year-round and book Facilitated sessions for quarterly events. Discounts apply when bundled.</div></div>
      <div class="faq-item"><button class="faq-q">How does the Edstellar training add-on work?</button><div class="faq-a">If you're already an Edstellar training client, Engage is added as a 15-20% uplift on the training contract. You get the same library plus reinforcement games auto-scheduled at 14 and 30 days post-training.</div></div>
      <div class="faq-item"><button class="faq-q">What payment methods do you accept?</button><div class="faq-a">Card, ACH, wire, invoice with NET-30. Enterprise contracts support PO-based invoicing in INR, USD, EUR, AED, SGD, GBP.</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="facil">
      <div>
        <h2>Need a custom quote?</h2>
        <p class="lead">For 2,000+ employees, multi-region rollouts, or training-bundle pricing - our team will put together a tailored plan in 24 hours.</p>
        <button class="btn btn-accent btn-lg" data-open-demo>Talk to Sales</button>
      </div>
      <div class="facil-table">
        <div class="facil-row"><span>Avg. setup time</span><b>5 minutes</b></div>
        <div class="facil-row"><span>Avg. activation in 14 days</span><b>55%</b></div>
        <div class="facil-row"><span>Custom quote turnaround</span><b>24 hours</b></div>
      </div>
    </div>
  </div>
</section>'''
page('pricing.html', 'Pricing - Edstellar Engage', PRICING_BODY, active_nav='./pricing.html')

# ---------------- USE CASES ----------------
USE_CASES_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">Use Cases</span>
    <h1>One platform. Four buyers. Four different ways to win.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">Each persona buys Engage for a different reason. We've built dedicated experiences for HR, L&amp;D, managers, and enterprise leaders.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="uc-grid" style="grid-template-columns:repeat(2,1fr);gap:20px">
      <div class="uc-card" id="hr">
        <span class="eyebrow" style="background:rgba(37,99,235,.1);color:var(--brand-accent-700)">HR Teams</span>
        <h3 style="margin:10px 0 8px">Run engagement programs that show up in HR metrics.</h3>
        <p>Onboarding quests, monthly culture games, recognition rituals, wellness campaigns. Engagement stops being a quarterly survey and starts being a weekly habit.</p>
        <h4 style="margin:14px 0 6px;font-size:13px;color:var(--brand-primary);text-transform:uppercase;letter-spacing:.04em">Top games for HR</h4>
        <ul>
          <li><a href="./game.html?id=onboarding-quest">Onboarding Quest</a> - 7-day new-hire game</li>
          <li><a href="./game.html?id=values-mapping">Values Mapping</a> - culture alignment</li>
          <li><a href="./game.html?id=stress-free-bingo">Stress-Free Bingo</a> - wellness habit builder</li>
        </ul>
        <a class="btn btn-primary btn-sm" href="./games.html?category=HR%20%2F%20Onboarding" style="margin-top:14px">Browse HR games →</a>
      </div>
      <div class="uc-card" id="ld">
        <span class="eyebrow" style="background:rgba(37,99,235,.1);color:var(--brand-accent-700)">L&amp;D Teams</span>
        <h3 style="margin:10px 0 8px">Make every training program 2× as effective.</h3>
        <p>Tie every Edstellar course to a reinforcement game at 14 and 30 days post-training. Beat the forgetting curve - without redesigning your LMS.</p>
        <h4 style="margin:14px 0 6px;font-size:13px;color:var(--brand-primary);text-transform:uppercase;letter-spacing:.04em">Top games for L&amp;D</h4>
        <ul>
          <li><a href="./game.html?id=sales-jeopardy">Sales Jeopardy</a> - post-sales-training reinforcement</li>
          <li><a href="./game.html?id=empathy-mapping">Empathy Mapping</a> - post-CX-training</li>
          <li><a href="./game.html?id=prioritization-pyramid">Prioritization Pyramid</a> - manager training follow-up</li>
        </ul>
        <a class="btn btn-primary btn-sm" href="./games.html?reinforces=1" style="margin-top:14px">Browse reinforcement games →</a>
      </div>
      <div class="uc-card" id="managers">
        <span class="eyebrow" style="background:rgba(37,99,235,.1);color:var(--brand-accent-700)">Managers</span>
        <h3 style="margin:10px 0 8px">Better 1:1s. Better team rituals. Less meeting-fatigue.</h3>
        <p>Trust Battery for quarterly check-ins, GROW coaching for monthly 1:1s, Hot Seat for project retros. Built for managers who want structure without slides.</p>
        <h4 style="margin:14px 0 6px;font-size:13px;color:var(--brand-primary);text-transform:uppercase;letter-spacing:.04em">Top games for Managers</h4>
        <ul>
          <li><a href="./game.html?id=trust-battery">Trust Battery</a> - quarterly trust check-in</li>
          <li><a href="./game.html?id=hot-seat">The Hot Seat</a> - project retro format</li>
          <li><a href="./game.html?id=leadership-pizza">Leadership Pizza</a> - team value alignment</li>
        </ul>
        <a class="btn btn-primary btn-sm" href="./games.html?category=Leadership" style="margin-top:14px">Browse leadership games →</a>
      </div>
      <div class="uc-card" id="enterprise">
        <span class="eyebrow" style="background:rgba(37,99,235,.1);color:var(--brand-accent-700)">Enterprise Leaders</span>
        <h3 style="margin:10px 0 8px">Measurable participation across every site and department.</h3>
        <p>Engagement trends, regional benchmarks, exportable dashboards. SSO, HRIS sync, regional data residency. Built for enterprise IT and compliance.</p>
        <h4 style="margin:14px 0 6px;font-size:13px;color:var(--brand-primary);text-transform:uppercase;letter-spacing:.04em">Top capabilities for Enterprise</h4>
        <ul>
          <li>Workspace branding + custom domains</li>
          <li>Department-level rollups and benchmarks</li>
          <li>Audit trails + SOC2-ready data handling</li>
        </ul>
        <a class="btn btn-primary btn-sm" href="./pricing.html" style="margin-top:14px">See Enterprise plan →</a>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border);border-bottom:1px solid var(--brand-border)">
  <div class="container">
    <h2>Why every persona buys for a different reason.</h2>
    <p class="lead">The same game can answer different objections depending on who's reading the spec.</p>
    <div class="compare" style="margin-top:20px">
      <table>
        <thead><tr><th>Question</th><th>HR</th><th>L&amp;D</th><th>Manager</th><th>Enterprise</th></tr></thead>
        <tbody>
          <tr><td>Primary outcome</td><td>Culture &amp; retention</td><td>Training ROI</td><td>Team health</td><td>Measurable engagement</td></tr>
          <tr><td>Top metric</td><td>eNPS / participation</td><td>Knowledge retention</td><td>1:1 quality</td><td>Activation %</td></tr>
          <tr><td>Procurement path</td><td>HR budget</td><td>L&amp;D budget</td><td>Manager discretion</td><td>Centralized buy</td></tr>
          <tr><td>Killer feature</td><td>Onboarding Quest</td><td>Reinforcement bundle</td><td>Trust Battery</td><td>SSO + dashboards</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="facil">
      <div>
        <h2>Not sure which persona fits your org?</h2>
        <p class="lead">A 20-minute demo, tailored to your role. We'll preload the games and reports that matter to your seat.</p>
        <button class="btn btn-accent btn-lg" data-open-demo>Book a Demo</button>
      </div>
      <div class="facil-table">
        <div class="facil-row"><span>HR-led pilots</span><b>14-day free trial</b></div>
        <div class="facil-row"><span>L&amp;D bundles</span><b>15-20% training add-on</b></div>
        <div class="facil-row"><span>Enterprise</span><b>Custom quote</b></div>
      </div>
    </div>
  </div>
</section>'''
page('use-cases.html', 'Use Cases - Edstellar Engage', USE_CASES_BODY, active_nav='./use-cases.html')

# ---------------- HOW IT WORKS ----------------
HOW_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">How it works</span>
    <h1>Five minutes to set up. Five beats to a great session.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">Admins schedule and walk away. The platform runs the session, surfaces debrief questions, and re-runs the game as reinforcement weeks later.</p>
    <div class="hero-cta" style="justify-content:center"><button class="btn btn-primary btn-lg" data-open-demo>Book a Demo</button><a class="btn btn-ghost btn-lg" href="./games.html">Browse games</a></div>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="container">
    <h2 style="text-align:center">Anatomy of a session</h2>
    <p class="lead" style="text-align:center;max-width:600px;margin:0 auto 8px">A typical Engage session has five beats from setup to debrief in 30 minutes.</p>
    <div class="timeline">
      <div class="tl-step"><div class="tl-marker">01</div><h4>Schedule</h4><p>Admin picks a game, invites teams, sets the date. Two minutes total.</p></div>
      <div class="tl-step"><div class="tl-marker">02</div><h4>Walkthrough</h4><p>Players see a 4-step popup explaining concept, rules, and the debrief questions.</p></div>
      <div class="tl-step"><div class="tl-marker">03</div><h4>Play</h4><p>Live or async. Leaderboards, timers, and team rooms run automatically.</p></div>
      <div class="tl-step"><div class="tl-marker">04</div><h4>Debrief</h4><p>The platform surfaces three structured review questions tied to the game.</p></div>
      <div class="tl-step"><div class="tl-marker">05</div><h4>Reinforce</h4><p>At 14 and 30 days post-training, the matching game re-runs on autopilot.</p></div>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border);border-bottom:1px solid var(--brand-border)">
  <div class="container" data-tab-scope>
    <h2>The two flows that matter.</h2>
    <p class="lead">For admins, setup is five minutes. For employees, joining is one click.</p>
    <div class="tabs" role="tablist" style="margin-top:18px">
      <button class="tab-btn active" data-tab="admins">For Admins</button>
      <button class="tab-btn" data-tab="employees">For Employees</button>
    </div>
    <div class="tab-panel active" data-panel="admins">
      <div class="steps">
        <div class="step"><div class="step-num">1</div><h3>Create your workspace</h3><p class="muted">Sign up, brand it with your colors and logo, invite admins. SSO supported on Business+.</p></div>
        <div class="step"><div class="step-num">2</div><h3>Pick games &amp; schedule</h3><p class="muted">Choose from 200+ games. Schedule live or async, assign teams, set reinforcement triggers.</p></div>
        <div class="step"><div class="step-num">3</div><h3>Track outcomes</h3><p class="muted">Participation, leaderboards, engagement trends. Export reports for HR or QBRs.</p></div>
      </div>
    </div>
    <div class="tab-panel" data-panel="employees">
      <div class="steps">
        <div class="step"><div class="step-num">1</div><h3>Join with one click</h3><p class="muted">Email invite or SSO. No new password to manage. Mobile and web supported.</p></div>
        <div class="step"><div class="step-num">2</div><h3>Play live or async</h3><p class="muted">Drop in for live games or take part in monthly campaigns on your time.</p></div>
        <div class="step"><div class="step-num">3</div><h3>Earn recognition</h3><p class="muted">Points, badges, leaderboards, peer shout-outs your manager can see in 1:1s.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>What's under the hood.</h2>
    <p class="lead">A handful of mechanics power 80% of the 200+ game library.</p>
    <div class="value-grid" style="margin-top:24px">
      <div class="value-card"><h3>Quiz &amp; trivia engine</h3><p class="muted">Live host console, buzz-in, scoring, leaderboards, async mode. Powers Sales Jeopardy, Product Knowledge, Customer Service quizzes.</p></div>
      <div class="value-card"><h3>Canvas &amp; mapping</h3><p class="muted">Sticky notes, drag-drop, shared boards. Powers Empathy Map, Vision Board, Force-Field Analysis, Values Mapping.</p></div>
      <div class="value-card"><h3>Voting &amp; consensus</h3><p class="muted">Dot voting, ranked-choice, weighted. Powers decision games, retros, prioritization exercises.</p></div>
      <div class="value-card"><h3>Bingo &amp; checklist</h3><p class="muted">Async habit games. Powers Stress-Free Bingo, Sales Bingo, Work Bingo, Wellness campaigns.</p></div>
      <div class="value-card"><h3>Role-play prompts</h3><p class="muted">Text + image + optional video scenarios. Powers Sell Me This Pen, Persuasion Roleplay, Hot Seat.</p></div>
      <div class="value-card"><h3>Anonymous submission</h3><p class="muted">Trust Box, Accountability Game, anonymous feedback. Psychological safety on by default.</p></div>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border)">
  <div class="container">
    <h2>Integrations.</h2>
    <p class="lead">Engage works with the tools your teams already use.</p>
    <div class="compare" style="margin-top:20px">
      <table>
        <thead><tr><th>Integration</th><th>Category</th><th>Available in</th></tr></thead>
        <tbody>
          <tr><td>Slack</td><td>Collaboration</td><td class="check">Team+</td></tr>
          <tr><td>Microsoft Teams</td><td>Collaboration</td><td class="check">Team+</td></tr>
          <tr><td>Google Workspace SSO</td><td>Identity</td><td class="check">Team+</td></tr>
          <tr><td>SAML / Okta / Azure AD</td><td>Identity</td><td class="check">Business+</td></tr>
          <tr><td>Workday</td><td>HRIS</td><td class="check">Business+</td></tr>
          <tr><td>BambooHR</td><td>HRIS</td><td class="check">Business+</td></tr>
          <tr><td>SCORM 1.2 / xAPI</td><td>LMS</td><td class="check">Enterprise</td></tr>
          <tr><td>Edstellar LMS catalog</td><td>Training</td><td class="check">All plans</td></tr>
          <tr><td>Zoom / Google Meet</td><td>Video</td><td class="partial">Phase 2</td></tr>
          <tr><td>Zapier / Make</td><td>Automation</td><td class="partial">Phase 2</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>'''
page('how-it-works.html', 'How it works - Edstellar Engage', HOW_BODY, active_nav='./how-it-works.html')

# ---------------- FACILITATED ----------------
FACIL_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">Facilitated Sessions</span>
    <h1>Trained Edstellar facilitators. Your big moments.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">For town halls, off-sites, leadership retreats, sales kickoffs, and onboarding waves - we bring a facilitator, a tailored game, and a debrief report.</p>
    <div class="hero-cta" style="justify-content:center"><button class="btn btn-accent btn-lg" data-open-demo>Book a Facilitator</button><a class="btn btn-ghost btn-lg" href="#packages">See packages</a></div>
  </div>
</section>

<section class="section" id="packages" style="padding-top:8px">
  <div class="container">
    <h2>Session tiers</h2>
    <p class="lead">Pricing scales with group size and customization. Every tier includes a facilitator, a tailored game, and a post-session debrief report.</p>
    <div class="price-grid" style="margin-top:24px">
      <div class="price-card">
        <h3>Standard</h3>
        <div class="price-amount">$1,500<small> / session</small></div>
        <p class="muted">Up to 50 participants</p>
        <ul class="price-feat">
          <li>1 Edstellar facilitator</li>
          <li>Templated game format</li>
          <li>60-90 minutes</li>
          <li>Virtual or hybrid</li>
          <li>Post-session report</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Book Session</button>
      </div>
      <div class="price-card popular">
        <span class="price-ribbon">MOST BOOKED</span>
        <h3>Standard+</h3>
        <div class="price-amount">$2,500<small> / session</small></div>
        <p class="muted">Up to 100 participants</p>
        <ul class="price-feat">
          <li>1 Edstellar facilitator</li>
          <li>Choice of 6 templated games</li>
          <li>60-90 minutes</li>
          <li>Virtual, hybrid, or in-person</li>
          <li>Detailed engagement report</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Book Session</button>
      </div>
      <div class="price-card">
        <h3>Premium custom</h3>
        <div class="price-amount">$4,000<small> / session</small></div>
        <p class="muted">Up to 100 participants</p>
        <ul class="price-feat">
          <li>2 facilitators</li>
          <li>Custom game design</li>
          <li>90-120 minutes</li>
          <li>Pre-session discovery call</li>
          <li>Full debrief + recommendations</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Book Session</button>
      </div>
      <div class="price-card">
        <h3>Enterprise event</h3>
        <div class="price-amount">$8K-$15K<small> / event</small></div>
        <p class="muted">200+ participants</p>
        <ul class="price-feat">
          <li>3+ facilitators, multi-room</li>
          <li>Fully custom design + branding</li>
          <li>Half-day or full-day formats</li>
          <li>Travel-included options</li>
          <li>Custom outcome report</li>
        </ul>
        <button class="btn btn-primary" data-open-demo>Talk to Sales</button>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border);border-bottom:1px solid var(--brand-border)">
  <div class="container">
    <h2>Where we deliver.</h2>
    <p class="lead">Edstellar's facilitator network covers 35+ countries with local-language delivery.</p>
    <div class="value-grid" style="margin-top:24px">
      <div class="value-card"><h3>India</h3><p class="muted">English, Hindi, Tamil, Telugu, Kannada. Same-week scheduling in major metros.</p></div>
      <div class="value-card"><h3>MEA</h3><p class="muted">English, Arabic. Strong presence in UAE, KSA, Egypt, South Africa.</p></div>
      <div class="value-card"><h3>APAC</h3><p class="muted">English plus local languages in Singapore, Philippines, Indonesia, Vietnam.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:820px">
    <h2>Common questions</h2>
    <div style="margin-top:18px">
      <div class="faq-item"><button class="faq-q">How fast can we book a session?</button><div class="faq-a">Standard sessions: 1-2 weeks lead time. Premium custom: 3-4 weeks. Enterprise events: 6-8 weeks. Rush is possible with a surcharge.</div></div>
      <div class="faq-item"><button class="faq-q">Can we use our own facilitators?</button><div class="faq-a">Yes. Edstellar can certify your internal facilitators through a 2-3 day Engage Facilitator program. Then you run on the platform with your own team.</div></div>
      <div class="faq-item"><button class="faq-q">What does the debrief report include?</button><div class="faq-a">Engagement metrics, qualitative themes, facilitator observations, top-rated activities, and 2-3 recommended follow-up actions for your team.</div></div>
      <div class="faq-item"><button class="faq-q">Can a session be recorded?</button><div class="faq-a">Yes with participant consent. We can also share anonymized highlights for internal sharing.</div></div>
    </div>
  </div>
</section>'''
page('facilitated.html', 'Facilitated Sessions - Edstellar Engage', FACIL_BODY)

# ---------------- COMPARE ----------------
COMPARE_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">Compare</span>
    <h1>How Engage stacks up.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">Most HR teams already have a quiz tool. The question is what to add on top - a polling app, an event service, or a full engagement platform tied to your training catalog.</p>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="container">
    <div class="compare">
      <table aria-label="Feature comparison">
        <thead>
          <tr>
            <th>Capability</th>
            <th class="col-engage">Edstellar Engage</th>
            <th>Kahoot at Work</th>
            <th>Mentimeter</th>
            <th>Gametize</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>200+ game library</td><td class="col-engage check">✓</td><td class="cross">limited</td><td class="cross">polls only</td><td class="partial">~</td></tr>
          <tr><td>Post-training reinforcement bundle</td><td class="col-engage check">✓ native</td><td class="cross">-</td><td class="cross">-</td><td class="cross">-</td></tr>
          <tr><td>Edstellar facilitator network</td><td class="col-engage check">✓ included</td><td class="cross">-</td><td class="cross">-</td><td class="cross">-</td></tr>
          <tr><td>Tied to an L&amp;D training catalog</td><td class="col-engage check">✓</td><td class="cross">-</td><td class="cross">-</td><td class="cross">-</td></tr>
          <tr><td>In-game currency &amp; power-ups</td><td class="col-engage check">✓ EngageCoins</td><td class="cross">-</td><td class="cross">-</td><td class="partial">~</td></tr>
          <tr><td>India / MEA / APAC delivery</td><td class="col-engage check">✓ strong</td><td class="partial">~</td><td class="partial">~</td><td class="cross">thin</td></tr>
          <tr><td>Live quiz format</td><td class="col-engage check">✓</td><td class="check">✓</td><td class="check">✓</td><td class="partial">~</td></tr>
          <tr><td>Async &amp; multi-week campaigns</td><td class="col-engage check">✓</td><td class="cross">-</td><td class="cross">-</td><td class="check">✓</td></tr>
          <tr><td>HRIS sync (Workday, BambooHR)</td><td class="col-engage check">✓ Enterprise</td><td class="cross">-</td><td class="cross">-</td><td class="partial">~</td></tr>
          <tr><td>Facilitated event services</td><td class="col-engage check">✓</td><td class="cross">-</td><td class="cross">-</td><td class="cross">-</td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted" style="margin-top:14px;font-size:13px;text-align:center">Comparison reflects publicly listed feature sets. Most clients keep Kahoot for quizzes and add Engage for everything around them.</p>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border);border-bottom:1px solid var(--brand-border)">
  <div class="container">
    <h2>The differences that actually matter.</h2>
    <p class="lead">Six reasons buyers tell us they picked Engage in evaluations.</p>
    <div class="value-grid" style="margin-top:24px">
      <div class="value-card"><h3>1. Tied to training</h3><p class="muted">Every game maps to an Edstellar course. Reinforcement happens automatically - you don't rebuild it in your LMS.</p></div>
      <div class="value-card"><h3>2. A real game library</h3><p class="muted">200+ games across 14 categories. Most competitors are quiz tools dressed up with a few extras.</p></div>
      <div class="value-card"><h3>3. Facilitators included</h3><p class="muted">Kahoot doesn't run your town hall. Engage facilitators do - at a fraction of agency rates.</p></div>
      <div class="value-card"><h3>4. Async + live</h3><p class="muted">Most competitors are live-only. Engage runs multi-week campaigns, async cohorts, and live sessions in one platform.</p></div>
      <div class="value-card"><h3>5. India, MEA, APAC strong</h3><p class="muted">Local facilitators, local-language delivery, local data residency. Built where Edstellar is strongest.</p></div>
      <div class="value-card"><h3>6. Buyer-aware</h3><p class="muted">Different value props for HR, L&amp;D, managers, and enterprise. Not "one feature page fits all".</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="facil">
      <div>
        <h2>Switching from Kahoot, Mentimeter, or Gametize?</h2>
        <p class="lead">We've migrated 40+ teams over. Import your existing quizzes, keep your branding, and bundle in reinforcement at the same contract value.</p>
        <button class="btn btn-accent btn-lg" data-open-demo>Talk to a Migration Specialist</button>
      </div>
      <div class="facil-table">
        <div class="facil-row"><span>Avg. migration</span><b>2-3 weeks</b></div>
        <div class="facil-row"><span>Avg. cost change</span><b>−12% bundled</b></div>
        <div class="facil-row"><span>Avg. engagement lift</span><b>+38% YoY</b></div>
      </div>
    </div>
  </div>
</section>'''
page('compare.html', 'Compare Engage - Edstellar Engage vs Kahoot, Mentimeter, Gametize', COMPARE_BODY, active_nav='./compare.html')

# ---------------- CASE STUDIES ----------------
CASES_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">Case Studies</span>
    <h1>How HR &amp; L&amp;D leaders use Engage.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">Three stories from the field - what they tried before Engage, what they ran, and what changed.</p>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="container">
    <div class="quotes" style="grid-template-columns:1fr;gap:24px;max-width:880px;margin:0 auto">

      <article class="quote" style="padding:32px">
        <h2 style="margin-top:0">Bangalore-based SaaS company adds Engage to a sales academy. Reinforcement attach hits 32% in Q1.</h2>
        <div class="compare" style="margin:18px 0">
          <table>
            <thead><tr><th>Metric</th><th>Before</th><th>After 90 days</th></tr></thead>
            <tbody>
              <tr><td>Sales training completion</td><td>71%</td><td class="check">94%</td></tr>
              <tr><td>30-day retention quiz score</td><td>54%</td><td class="check">82%</td></tr>
              <tr><td>Reinforcement attach</td><td>0%</td><td class="check">32%</td></tr>
            </tbody>
          </table>
        </div>
        <p><strong>Setup:</strong> Bundled Engage with their existing sales training contract. Used Sales Jeopardy at 14 days post-training and Empathy Mapping at 30 days. Both games re-ran automatically.</p>
        <p><strong>What worked:</strong> Reps started bragging about leaderboard rank in standups. Sales ops stopped chasing CRM hygiene because Sales Bingo did it for them.</p>
        <div class="quote-author">
          <span class="quote-avatar">PR</span>
          <div><strong>Priya R.</strong><small>Head of L&amp;D · Mid-market SaaS, Bangalore</small></div>
        </div>
      </article>

      <article class="quote" style="padding:32px">
        <h2 style="margin-top:0">Regional bank in Dubai replaces PowerPoint town-hall games with facilitated Engage sessions.</h2>
        <div class="compare" style="margin:18px 0">
          <table>
            <thead><tr><th>Metric</th><th>Before</th><th>After 6 months</th></tr></thead>
            <tbody>
              <tr><td>Design time per session</td><td>18 hours</td><td class="check">15 minutes</td></tr>
              <tr><td>Avg. participation</td><td>64%</td><td class="check">89%</td></tr>
              <tr><td>Town hall NPS</td><td>22</td><td class="check">58</td></tr>
            </tbody>
          </table>
        </div>
        <p><strong>Setup:</strong> Standard+ Facilitated tier monthly for 100-person town halls. Arabic + English facilitator. Engage facilitator certified two internal HRBPs for in-between events.</p>
        <p><strong>What worked:</strong> No more last-minute slide builds. Town halls felt fresh because each one used a different game from the library.</p>
        <div class="quote-author">
          <span class="quote-avatar">SM</span>
          <div><strong>Salah M.</strong><small>HR Director · Regional bank, Dubai</small></div>
        </div>
      </article>

      <article class="quote" style="padding:32px">
        <h2 style="margin-top:0">Singapore logistics co. uses EngageCoins on Egg Drop. People who never engaged with Kahoot start sending each other coins.</h2>
        <div class="compare" style="margin:18px 0">
          <table>
            <thead><tr><th>Metric</th><th>Before</th><th>After 90 days</th></tr></thead>
            <tbody>
              <tr><td>Monthly Active Employees</td><td>22%</td><td class="check">61%</td></tr>
              <tr><td>Peer recognition events / wk</td><td>4</td><td class="check">87</td></tr>
              <tr><td>Engagement survey eNPS</td><td>11</td><td class="check">37</td></tr>
            </tbody>
          </table>
        </div>
        <p><strong>Setup:</strong> Business plan with currency mechanic enabled on three games (Egg Drop, Sales Jeopardy, Onboarding Quest). Quarterly leaderboard prizes via gift cards.</p>
        <p><strong>What worked:</strong> The currency was the trigger. Once people figured out generosity earned coins too, the recognition culture shifted on its own.</p>
        <div class="quote-author">
          <span class="quote-avatar">JT</span>
          <div><strong>Jenna T.</strong><small>People Ops Lead · Logistics, Singapore</small></div>
        </div>
      </article>

    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="facil">
      <div>
        <h2>Want a case study built around your stack?</h2>
        <p class="lead">If you're a pilot account, we co-author your case study at the 90-day mark. Your wins, your numbers, your screenshots.</p>
        <button class="btn btn-accent btn-lg" data-open-demo>Apply for a Pilot</button>
      </div>
      <div class="facil-table">
        <div class="facil-row"><span>Pilot length</span><b>60 days free</b></div>
        <div class="facil-row"><span>Case study turnaround</span><b>2 weeks</b></div>
        <div class="facil-row"><span>Co-marketing perks</span><b>Webinar + logo</b></div>
      </div>
    </div>
  </div>
</section>'''
page('case-studies.html', 'Case Studies - Edstellar Engage', CASES_BODY)

# ---------------- ABOUT ----------------
ABOUT_BODY = '''<section class="hero" style="padding:72px 0 32px">
  <div class="container" style="max-width:920px;text-align:center">
    <span class="eyebrow">About</span>
    <h1>Built for the gap between training and behavior.</h1>
    <p class="lead" style="margin:14px auto 24px;max-width:680px">Edstellar Engage is the engagement and reinforcement product inside the Edstellar talent-transformation suite. We make training stick - by turning it into a game your team actually plays.</p>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="container">
    <div class="value-grid">
      <div class="value-card"><h3>What we are</h3><p class="muted">A SaaS-plus-services product. Platform for engagement programs. Facilitator network for live events. Tied to the world's largest curated training catalog.</p></div>
      <div class="value-card"><h3>What we're not</h3><p class="muted">Not a quiz tool. Not a polling app. Not an entertainment site. We don't replace Kahoot for live quizzes - we wrap engagement around what your training delivers.</p></div>
      <div class="value-card"><h3>Where we come from</h3><p class="muted">Edstellar has delivered training to 500K+ professionals across 200+ enterprises in India, MEA, APAC, and Europe. Engage is what those clients asked us to build.</p></div>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border);border-bottom:1px solid var(--brand-border)">
  <div class="container">
    <h2>By the numbers.</h2>
    <p class="lead">Engagement is a P&amp;L line item. We treat it like one.</p>
    <div class="stats-strip" style="grid-template-columns:repeat(4,1fr);margin-top:24px">
      <div class="stat-card"><div class="stat-num">200+</div><div class="stat-label">Games in the library</div></div>
      <div class="stat-card"><div class="stat-num">14</div><div class="stat-label">Categories covered</div></div>
      <div class="stat-card"><div class="stat-num">35+</div><div class="stat-label">Countries served by facilitators</div></div>
      <div class="stat-card"><div class="stat-num">500K+</div><div class="stat-label">Edstellar training participants</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Why engagement, why now.</h2>
    <p class="lead">Three numbers we cite a lot, and what they mean.</p>
    <div class="stats-strip" style="margin-top:24px">
      <div class="stat-card"><div class="stat-num">21%</div><div class="stat-label">of employees globally are engaged (Gallup 2024). Engagement isn't an HR nice-to-have - it's the default failure mode of modern work.</div></div>
      <div class="stat-card"><div class="stat-num">50%</div><div class="stat-label">of training content is forgotten within 1 hour (Ebbinghaus). Without reinforcement, your training spend evaporates fast.</div></div>
      <div class="stat-card"><div class="stat-num">$438B</div><div class="stat-label">in annual economic loss from disengagement (Gallup). Engage exists to convert a fraction of that into measurable wins.</div></div>
    </div>
  </div>
</section>

<section class="section" style="background:#fff;border-top:1px solid var(--brand-border)">
  <div class="container">
    <h2>Where we're headed.</h2>
    <p class="lead">Roadmap themes we're investing in over the next 12 months.</p>
    <div class="value-grid" style="margin-top:24px">
      <div class="value-card"><h3>Cross-game wallet</h3><p class="muted">EngageCoins persist across games at the workspace level. Manager-allocated budgets. Redemption catalog (gift cards, donations, training credits).</p></div>
      <div class="value-card"><h3>AI walkthroughs</h3><p class="muted">Auto-generated, per-game player walkthroughs adapted to the user's role, language, and prior history.</p></div>
      <div class="value-card"><h3>Real-time benchmarks</h3><p class="muted">Industry-wide engagement benchmarks anonymized across the customer base. Compare to your peer group.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="facil">
      <div>
        <h2>Want to talk?</h2>
        <p class="lead">We'd love to hear about your team. 20-minute demo, no pitch deck.</p>
        <button class="btn btn-accent btn-lg" data-open-demo>Book a Demo</button>
      </div>
      <div class="facil-table">
        <div class="facil-row"><span>Headquarters</span><b>Bangalore, India</b></div>
        <div class="facil-row"><span>Edstellar website</span><b><a href="https://www.edstellar.com" target="_blank" rel="noopener" style="color:var(--brand-accent)">edstellar.com</a></b></div>
        <div class="facil-row"><span>Engage email</span><b style="color:var(--brand-accent)">engage@edstellar.com</b></div>
      </div>
    </div>
  </div>
</section>'''
page('about.html', 'About - Edstellar Engage', ABOUT_BODY)

print('\nAll pages generated.')
