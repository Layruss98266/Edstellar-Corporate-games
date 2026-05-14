"""
Parse Edstellar_Engage_All_Games_Master.html and produce:
- engage-prototype/assets/games.json
- engage-prototype/assets/games-data.js (loads as a script for file:// usage)

Run from the repo root:
  python engage-prototype/_build/parse_master.py

Re-runnable. No external deps - regex-based parsing of the master HTML's
highly regular machine-generated structure.
"""
from __future__ import annotations
import html as ihtml
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # repo root
MASTER = ROOT / "Edstellar_Engage_All_Games_Master.html"
OUT_JSON = HERE.parent / "assets" / "games.json"
OUT_JS = HERE.parent / "assets" / "games-data.js"

# Blog index 1..14 -> category in the prototype taxonomy
BLOG_CATEGORY = {
    1: "HR / Onboarding",
    2: "Performance Management",
    3: "Stress / Wellness",
    4: "Decision Making",
    5: "Change Management",
    6: "Sales",
    7: "Leadership",
    8: "Customer Service",
    9: "Critical Thinking",
    10: "Accountability",
    11: "Time Management",
    12: "Communication",
    13: "Problem Solving",
    14: "Goal Setting",
}

# Category -> default audience tags
AUDIENCE = {
    "Sales": ["Sales"],
    "Customer Service": ["Customer Service"],
    "Leadership": ["Managers", "Leaders"],
    "HR / Onboarding": ["All employees", "New hires"],
    "Stress / Wellness": ["All employees"],
    "Accountability": ["Managers", "All employees"],
    "Change Management": ["Managers", "Leaders"],
    "Performance Management": ["Managers", "All employees"],
    "Decision Making": ["Leaders", "Managers"],
    "Critical Thinking": ["All employees"],
    "Problem Solving": ["All employees"],
    "Time Management": ["All employees"],
    "Communication": ["All employees", "New hires"],
    "Goal Setting": ["All employees", "Managers"],
}

# Category -> linked Edstellar training program (used when reinforcesTraining=True)
TRAINING = {
    "Sales": ("Sales Excellence Training", "https://www.edstellar.com/course/sales-training"),
    "Leadership": ("Leadership Development", "https://www.edstellar.com/course/leadership-training"),
    "Customer Service": ("Customer Service Excellence", "https://www.edstellar.com/course/customer-service-training"),
    "Performance Management": ("Performance Management Essentials", "https://www.edstellar.com/course/performance-management"),
    "Change Management": ("Change Management", "https://www.edstellar.com/course/change-management"),
    "Communication": ("Effective Communication", "https://www.edstellar.com/course/communication-skills-training"),
    "Decision Making": ("Strategic Thinking", "https://www.edstellar.com/course/strategic-thinking"),
    "Goal Setting": ("Goal Setting and OKRs", "https://www.edstellar.com/course/goal-setting"),
    "Time Management": ("Time Management Mastery", "https://www.edstellar.com/course/time-management"),
    "Critical Thinking": ("Critical Thinking", "https://www.edstellar.com/course/critical-thinking"),
    "Problem Solving": ("Problem Solving", "https://www.edstellar.com/course/problem-solving"),
    "Stress / Wellness": ("Workplace Wellness", "https://www.edstellar.com/course/stress-management"),
    "Accountability": ("Accountability at Work", "https://www.edstellar.com/course/accountability"),
    "HR / Onboarding": ("Employee Onboarding", "https://www.edstellar.com/course/onboarding"),
}

# Slug uniqueness map (populated during parse)
USED_SLUGS: set[str] = set()

# ---------- Helpers ----------
def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def unique_slug(base: str, gid: str) -> str:
    if base and base not in USED_SLUGS:
        USED_SLUGS.add(base)
        return base
    candidate = f"{base}-{gid}".strip("-")
    USED_SLUGS.add(candidate)
    return candidate

def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return ihtml.unescape(s).strip()

def first(pattern: str, text: str, flags=re.S) -> str:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""

def list_items(html_chunk: str) -> list[str]:
    return [strip_tags(m.group(1)) for m in re.finditer(r"<li[^>]*>(.*?)</li>", html_chunk or "", re.S)]

def field_text(label: str, article_html: str) -> str:
    # Match: <div class="field"><div class="label">LABEL</div><div class="value">VALUE</div></div>
    pat = (
        r'<div class="field">\s*<div class="label">'
        + re.escape(label)
        + r'</div>\s*<div class="value">(.*?)</div>\s*</div>'
    )
    return strip_tags(first(pat, article_html))

def field_list(label: str, article_html: str, list_tag: str) -> list[str]:
    pat = (
        r'<div class="field">\s*<div class="label">'
        + re.escape(label)
        + r'</div>\s*<' + list_tag + r'[^>]*>(.*?)</' + list_tag + r'>\s*</div>'
    )
    chunk = first(pat, article_html)
    return list_items(chunk)

# ---------- Schema normalization ----------
DURATION_BUCKETS = [
    (r"\bunder\s*15|\b<\s*15|0-15", "<15"),
    (r"\b15[--]20|15[--]30", "15-30"),
    (r"\b30[--]45|30[--]60|30 min cycles", "30-60"),
    (r"\b60\+|45[--]60|ongoing|7-day|day cohort", "60+"),
    (r"\b15 min\b|\b15 minutes\b", "<15"),
    (r"\b30 min\b|\b30 minutes\b", "15-30"),
]
def duration_bucket(duration: str) -> str:
    d = duration.lower()
    for pat, val in DURATION_BUCKETS:
        if re.search(pat, d):
            return val
    return "15-30"

def team_bucket(team: str) -> str:
    t = team.lower()
    # Solo
    if re.search(r"\b1\b(?!\d)|\bsolo\b|\bindividual\b", t) and not re.search(r"-|\bto\b|\+", t):
        return "1"
    # Try to pull max from "3-6", "5+", "Any"
    if re.search(r"\bany\b|\b50\+|10\s*-\s*\d{2,}|20\+|100\+", t):
        return "50+"
    m = re.search(r"(\d+)\s*[--]\s*(\d+)", t)
    if m:
        hi = int(m.group(2))
        if hi <= 10: return "2-10"
        if hi <= 50: return "10-50"
        return "50+"
    if re.search(r"\b50\+|\b100\+|\bunlimited", t):
        return "50+"
    return "2-10"

def derive_format(title: str, type_tag: str) -> str:
    name = title.lower()
    if any(k in name for k in ["bingo","pomodoro","kanban","vision board","async","bingo","quest","streak","journal","habit","onboarding quest"]):
        return "Async"
    if any(k in name for k in ["scavenger hunt","escape room","facilitated"]):
        return "Live"
    if "case study" in (type_tag or "").lower():
        return "Async"
    if "exercise" in (type_tag or "").lower():
        return "Live"
    return "Live"

def derive_difficulty(title: str, type_tag: str) -> str:
    name = title.lower()
    if "case study" in (type_tag or "").lower():
        return "Easy"
    if any(k in name for k in ["murder mystery","red team","crisis","strategic","negotiation","ethical dilemma"]):
        return "Hard"
    if any(k in name for k in ["breath","stretch","bingo","name game","two truths","walk"]):
        return "Easy"
    return "Medium"

def derive_reinforces(category: str, title: str, biz_purpose: str) -> bool:
    # Reinforcement-friendly categories
    if category in ("Sales","Leadership","Customer Service","Performance Management","Change Management","Communication","Goal Setting"):
        return True
    # Inspect biz purpose for explicit training language
    if re.search(r"reinforce|training|onboard|learning", (biz_purpose or "").lower()):
        return True
    return False

# Special hand-tuned economies for marquee games.
ECONOMY_OVERRIDES = {
    "egg-drop": {
        "currency": "EngageCoins",
        "starting": 200,
        "explainer": "Each team gets a virtual budget. Buy materials carefully - overspending leaves no margin for backup ideas, but cheap-only builds rarely survive the drop.",
        "earnRules": [
            "Help another team: +20 coins",
            "Share a design tip in chat: +10 coins",
            "Finish under budget bonus: +1 coin per unspent coin",
            "Egg survives the drop: +100 coins"
        ],
        "shop": [
            {"id":"ed-tape","name":"Roll of Tape","cost":30,"effect":"Bind materials together. The workhorse of every egg-drop build.","icon":"🩹"},
            {"id":"ed-string","name":"Ball of String","cost":20,"effect":"Suspend the egg inside a structure for shock absorption.","icon":"🪢"},
            {"id":"ed-foam","name":"Foam Padding","cost":50,"effect":"Absorbs impact. Limited supply.","icon":"🧱"},
            {"id":"ed-parachute","name":"Mini Parachute","cost":80,"effect":"Slow the descent. Single use, high impact.","icon":"🪂"},
            {"id":"ed-bubble","name":"Bubble Wrap","cost":40,"effect":"Wrap the egg directly. Reliable, popular choice.","icon":"📦"},
            {"id":"ed-straws","name":"Pack of Straws","cost":25,"effect":"Build a lightweight frame around the egg.","icon":"🥤"},
            {"id":"ed-popsicle","name":"Popsicle Sticks","cost":35,"effect":"Stiff frame material. Pair with tape.","icon":"🪵"},
            {"id":"ed-balloon","name":"Helium Balloon","cost":90,"effect":"Cuts effective drop speed by ~30%. Premium item.","icon":"🎈"}
        ]
    },
    "sales-jeopardy": {
        "currency": "EngageCoins",
        "starting": 150,
        "explainer": "Power-ups change the shape of a tough round. Save coins for the late game; high-value categories reward bold plays.",
        "earnRules": [
            "Correct answer: +25 coins",
            "Daily Double: +50 coins",
            "Final round winner: +100 coins"
        ],
        "shop": [
            {"id":"sj-hint","name":"50/50 Hint","cost":40,"effect":"Eliminate two wrong answers on a multiple-choice question.","icon":"💡"},
            {"id":"sj-double","name":"Double Points","cost":60,"effect":"Double your score on the next question (correct or wrong).","icon":"✕2"},
            {"id":"sj-steal","name":"Steal Power","cost":80,"effect":"Steal points from the leading team if they answer wrong.","icon":"⚡"},
            {"id":"sj-skip","name":"Skip & Re-roll","cost":30,"effect":"Skip a question your team isn't sure about. Re-roll a new one in the same category.","icon":"↻"}
        ]
    }
}

# Special title-keyed slugs (so the prototype's hand-picked games still resolve)
SLUG_PREFER = {
    "egg drop": "egg-drop",
    "egg drop challenge": "egg-drop",
    "sales jeopardy": "sales-jeopardy",
    "virtual escape room": "escape-room",
    "escape room": "escape-room",
    "stress-free bingo": "stress-free-bingo",
    "leadership pizza": "leadership-pizza",
    "empathy mapping": "empathy-mapping",
    "empathy mapping sessions": "empathy-mapping",
    "trust battery": "trust-battery",
    "trust battery exercise": "trust-battery",
    "sales bingo": "sales-bingo",
    "dot voting": "dot-voting",
    "prioritization pyramid": "prioritization-pyramid",
    "listen and draw": "listen-and-draw",
    "murder mystery": "murder-mystery",
    "pomodoro": "pomodoro-sprint",
    "vision board": "vision-board",
    "personal vision boards": "vision-board",
    "force-field analysis": "force-field-analysis",
    "the hot seat": "hot-seat",
    "red team vs. blue team": "red-blue-team",
    "red team vs. blue team exercise": "red-blue-team",
    "values mapping exercise": "values-mapping",
    "values mapping": "values-mapping",
}

# ---------- Parse ----------
def parse():
    if not MASTER.exists():
        print(f"ERROR: master file not found at {MASTER}", file=sys.stderr); sys.exit(1)
    text = MASTER.read_text(encoding="utf-8", errors="ignore")

    games: list[dict] = []

    # Each blog section: <section class="blog-block" id="blog-N">...</section>
    # But sections aren't strictly closed in the file. Split between "blog-N" markers.
    blog_markers = list(re.finditer(r'<section class="blog-block" id="blog-(\d+)"', text))
    for i, m in enumerate(blog_markers):
        blog_n = int(m.group(1))
        start = m.start()
        end = blog_markers[i+1].start() if i+1 < len(blog_markers) else len(text)
        block = text[start:end]

        category = BLOG_CATEGORY.get(blog_n, "HR / Onboarding")
        blog_title = strip_tags(first(r"<h2>([^<]+)</h2>", block))
        blog_url = first(r'<p class="source">Source:\s*<a[^>]+href="([^"]+)"', block)

        # Each article: <article class="card" id="..."> ... </article>
        for am in re.finditer(r'<article class="card"\s+id="([^"]+)">(.*?)</article>', block, re.S):
            article_id_attr = am.group(1)
            inner = am.group(2)

            # ID is the gNNN prefix
            gid_match = re.match(r"(g\d+)", article_id_attr)
            gid = gid_match.group(1) if gid_match else article_id_attr.split("-")[0]

            # Title from the first <h3> inside the article: "G007. Prioritization Pyramid"
            raw_title = strip_tags(first(r"<h3>(.*?)</h3>", inner))
            title = re.sub(r"^G\d+\.\s*", "", raw_title).strip()

            # Tags inside <div class="meta">...</div>
            meta_html = first(r'<div class="meta">(.*?)</div>', inner)
            tags = [strip_tags(t.group(1)) for t in re.finditer(r"<span[^>]*>(.*?)</span>", meta_html or "")]
            type_tag = tags[0] if len(tags) > 0 else "Activity"
            duration = tags[1] if len(tags) > 1 else "15-30 minutes"
            team = tags[2] if len(tags) > 2 else "3-6 participants per team"

            source_context = field_text("Source Context", inner)
            concept = field_text("Concept", inner)
            biz_purpose = field_text("Business Purpose", inner)
            skills_raw = field_text("Skills Developed", inner)
            materials = field_text("Materials / Setup", inner)
            how_to = field_list("How to Play", inner, "ol")
            review_qs = field_list("Review Questions", inner, "ul")
            key_take = field_text("Key Takeaway", inner)
            source_url = first(r'<p class="source">Source blog:\s*<a[^>]+href="([^"]+)"', inner) or blog_url

            skills = [s.strip() for s in re.split(r",", skills_raw) if s.strip()]

            # Slug
            preferred = SLUG_PREFER.get(title.lower().strip())
            base_slug = preferred or slugify(title)
            slug = unique_slug(base_slug, gid)

            # Derived fields
            fmt = derive_format(title, type_tag)
            diff = derive_difficulty(title, type_tag)
            reinforces = derive_reinforces(category, title, biz_purpose)

            audience = AUDIENCE.get(category, ["All employees"])
            training_program, training_url = TRAINING.get(category, (None, None))

            # Walkthrough - 4 steps derived from structured fields
            walkthrough = [
                {"title": "What is this game?", "body": concept or biz_purpose or "Workplace activity from the Edstellar library."},
                {"title": "How a round plays out",
                 "body": " ".join((f"Step {i+1}: {s}" for i, s in enumerate(how_to[:3]))) or "A facilitator guides the team through the activity step by step."},
                {"title": "Questions you'll discuss after",
                 "body": " ".join(f"• {q}" for q in (review_qs[:3] or ["What worked?", "What didn't?", "How will you apply this back at work?"]))},
                {"title": "Why this game matters",
                 "body": key_take or biz_purpose or "Every game in Edstellar Engage is built to drive real behavior change at work."}
            ]

            game = {
                "id": gid,
                "slug": slug,
                "title": title,
                "category": category,
                "audience": audience,
                "format": fmt,
                "duration": duration,
                "durationBucket": duration_bucket(duration),
                "team": team,
                "teamBucket": team_bucket(team),
                "difficulty": diff,
                "facilitator": "Recommended" if "Hard" == diff else "Optional",
                "reinforcesTraining": reinforces,
                "concept": concept,
                "businessPurpose": biz_purpose,
                "skills": skills,
                "materials": materials,
                "howToPlay": how_to,
                "reviewQuestions": review_qs,
                "keyTakeaway": key_take,
                "sourceContext": source_context,
                "sourceBlog": source_url,
                "sourceBlogTitle": blog_title,
                "type": type_tag,
                "walkthrough": walkthrough,
                # Legacy fields preserved for backwards compatibility:
                "outcomes": [s for s in [biz_purpose] if s] or ["Build skills through structured workplace activity."],
                "needs": {
                    "materials": materials or "Browser. Optional printables.",
                    "platform": "Engage facilitator console, timer, team rooms.",
                    "facilitator": "Recommended." if diff == "Hard" else "Optional."
                },
                "variations": [],
            }

            if reinforces and training_program:
                game["trainingProgram"] = training_program
                game["trainingUrl"] = training_url

            # Apply economy override if present
            if slug in ECONOMY_OVERRIDES:
                game["economy"] = ECONOMY_OVERRIDES[slug]

            games.append(game)

    print(f"Parsed {len(games)} games across {len(blog_markers)} blog sections.")
    return games

def write_outputs(games: list[dict]):
    payload = {"games": games}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    js = (
        "/* Auto-generated by engage-prototype/_build/parse_master.py.\n"
        "   Edit games.json (or the master HTML) and re-run the parser.\n"
        "   Loaded as a script so the prototype works from file:// - Chromium blocks fetch on file URLs. */\n"
        "window.GAMES_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n"
    )
    OUT_JS.write_text(js, encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)} ({OUT_JSON.stat().st_size} bytes)")
    print(f"Wrote {OUT_JS.relative_to(ROOT)} ({OUT_JS.stat().st_size} bytes)")

if __name__ == "__main__":
    games = parse()
    write_outputs(games)

    # Quick stats
    by_cat: dict[str,int] = {}
    for g in games: by_cat[g["category"]] = by_cat.get(g["category"], 0) + 1
    print("\nGames per category:")
    for c, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {c:<30} {n}")
    rt = sum(1 for g in games if g["reinforcesTraining"])
    print(f"\nReinforces training: {rt}/{len(games)}")
    eco = [g["slug"] for g in games if "economy" in g]
    print(f"With economy: {eco}")
