# Production migration plan

> Detailed plan for converting Edstellar Engage from `engage-prototype/` (vanilla HTML, single-device, localStorage) to a Next.js + Supabase production app. **Not started.** Reference doc until execution begins.

## Goal

Ship a production-ready `engage.edstellar.com` running on Next.js 15 + Supabase that supports real multi-device events: facilitator signs in, schedules an event, players join via short code on their phones, projector shows live scores, judge scores from a separate tab, debrief PDF generated automatically.

## Pilot-ready threshold

A real Edstellar customer can run an event end-to-end on the platform after:
- Phase 1 (Game Loop MVP) — one game runnable end-to-end
- Phase 2 (Realtime + Projector) — multi-device sync within 1s
- Essential Phase 4 items (signed cookies, rate-limited join codes)

Everything else is polish.

---

## What stays vs. what's new

| Path | Status |
|---|---|
| `engage-prototype/` | **Stays unchanged.** Sales/demo artifact. Runs from file:// for offline pitches. |
| `engage-app/` | **New.** Next.js 15 app. The production surface. |
| `supabase/` | **New.** Schema migrations + edge functions + seed data. |
| `.github/workflows/` | **New.** CI: TS check + lint + tests + build. |
| Root `vercel.json` | Updated to route `/` → engage-app, `/demo/*` → engage-prototype. |

## Stack (exact versions to pin)

```json
{
  "next": "^15.0.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5.6.0",
  "@supabase/ssr": "^0.10.0",
  "@supabase/supabase-js": "^2.45.0",
  "tailwindcss": "^4.0.0",
  "@tailwindcss/postcss": "^4.0.0",
  "shadcn": "^4.0.0",
  "@base-ui/react": "^1.4.0",
  "lucide-react": "^1.14.0",
  "react-hook-form": "^7.75.0",
  "zod": "^4.4.0",
  "recharts": "^3.8.0",
  "sonner": "^2.0.0",
  "next-themes": "^0.4.0",
  "clsx": "^2.1.0",
  "tailwind-merge": "^3.6.0",
  "class-variance-authority": "^0.7.0",
  "resend": "^4.0.0"
}
```

DevDeps: `vitest ^4`, `@testing-library/react ^16`, `@testing-library/dom ^10`, `jsdom ^29`, `@vitejs/plugin-react ^6`, `@playwright/test ^1.50`, `eslint ^9`, `eslint-config-next ^15`, `prettier ^3`, `@types/node ^20`, `@types/react ^19`.

Why this stack:
- Next.js 15 App Router — server components + server actions + edge runtime
- Supabase — Postgres + Auth + Realtime + Storage + Edge Functions in one
- shadcn/ui — copy-paste components on top of @base-ui (full ownership, no library lock-in)
- Tailwind v4 — config-less, native CSS variables
- react-hook-form + zod — best-in-class form layer
- recharts — debrief analytics
- sonner — toasts identical to prototype's `Shell.toast` API
- Resend — transactional email (3000/month free, then $20/mo)

## Environment variables

```bash
# Public (browser-safe)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_APP_URL=https://engage.edstellar.com

# Server-only (never reaches client)
SUPABASE_SERVICE_ROLE_KEY=          # bypasses RLS — use in server actions only
TEAM_SESSION_SECRET=                # HMAC key for signed team_session cookies
RESEND_API_KEY=                     # transactional email
SENTRY_DSN=                         # error tracking

# Build-time
SENTRY_AUTH_TOKEN=                  # source map upload
```

## Directory layout (target)

```
engage-app/
├── src/
│   ├── app/
│   │   ├── (marketing)/             # public pages — content same as prototype
│   │   │   ├── page.tsx             # landing
│   │   │   ├── games/page.tsx       # library
│   │   │   ├── games/[slug]/page.tsx
│   │   │   ├── pricing/page.tsx
│   │   │   ├── use-cases/page.tsx
│   │   │   ├── how-it-works/page.tsx
│   │   │   ├── facilitated/page.tsx
│   │   │   ├── compare/page.tsx
│   │   │   ├── case-studies/page.tsx
│   │   │   └── about/page.tsx
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   ├── forgot-password/page.tsx
│   │   │   ├── auth/callback/route.ts
│   │   │   └── auth/update-password/page.tsx
│   │   ├── (admin)/
│   │   │   ├── admin/
│   │   │   │   ├── page.tsx          # events list
│   │   │   │   ├── events/new/page.tsx
│   │   │   │   ├── events/[id]/
│   │   │   │   │   ├── layout.tsx
│   │   │   │   │   ├── page.tsx       # overview
│   │   │   │   │   ├── teams/page.tsx
│   │   │   │   │   ├── teams/[teamId]/page.tsx
│   │   │   │   │   ├── resources/page.tsx
│   │   │   │   │   ├── live/page.tsx  # H-key controls overlay
│   │   │   │   │   └── debrief/page.tsx
│   │   │   │   └── audit/page.tsx
│   │   ├── (judge)/judge/[eventId]/page.tsx
│   │   ├── (team)/team/
│   │   │   ├── page.tsx               # team console
│   │   │   └── join/page.tsx
│   │   ├── actions/                   # server actions ('use server')
│   │   │   ├── auth.ts
│   │   │   ├── events.ts
│   │   │   ├── teams.ts
│   │   │   ├── resources.ts
│   │   │   ├── game-engine.ts        # phase transitions
│   │   │   ├── scoring.ts             # per-game score submission
│   │   │   ├── two-truths.ts          # vote, reveal, statements
│   │   │   ├── egg-drop.ts            # purchase, drop-test, score
│   │   │   ├── improv.ts              # prompt, score round
│   │   │   ├── audit.ts
│   │   │   └── uploads.ts             # avatars to Supabase Storage
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/                        # shadcn primitives (button, card, dialog, …)
│   │   ├── game/
│   │   │   ├── realtime-timer.tsx
│   │   │   ├── phase-pill.tsx
│   │   │   ├── judge-gate.tsx
│   │   │   ├── team-card.tsx
│   │   │   ├── scoreboard-row.tsx
│   │   │   ├── leaderboard.tsx
│   │   │   ├── share-modal.tsx
│   │   │   └── confetti-canvas.tsx
│   │   ├── two-truths/
│   │   │   ├── statement-card.tsx
│   │   │   ├── private-editor.tsx
│   │   │   └── voter-queue.tsx
│   │   ├── egg-drop/
│   │   │   ├── material-card.tsx
│   │   │   ├── drop-zone.tsx
│   │   │   ├── drop-test-form.tsx
│   │   │   └── marketplace.tsx
│   │   ├── improv/
│   │   │   ├── prompt-card.tsx
│   │   │   ├── score-dots.tsx
│   │   │   └── coaching-tip.tsx
│   │   └── admin/
│   │       ├── event-header-controls.tsx
│   │       ├── live-screen.tsx
│   │       ├── controls-overlay.tsx
│   │       ├── live-ticker.tsx
│   │       └── teams-wizard.tsx
│   ├── hooks/
│   │   ├── use-event.ts
│   │   ├── use-teams.ts
│   │   ├── use-team.ts
│   │   ├── use-wallet.ts
│   │   ├── use-resources.ts
│   │   ├── use-scores.ts
│   │   ├── use-leaderboard.ts
│   │   ├── use-audit-log.ts
│   │   ├── use-event-phase.ts
│   │   ├── use-realtime-timer.ts
│   │   ├── use-session.ts
│   │   └── use-team-session.ts
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts              # anon key, browser
│   │   │   ├── server.ts              # anon key + cookies, SSR
│   │   │   └── admin.ts               # service role, server actions only
│   │   ├── constants.ts                # GAME_PHASES per game, TEAM_COLORS, etc.
│   │   ├── utils.ts                    # cn(), safe(), etc.
│   │   ├── email.ts                    # Resend wrapper
│   │   ├── jwt.ts                      # signed team_session
│   │   └── join-code.ts                # 32-char alphabet generator
│   ├── types/
│   │   ├── game.ts                     # Event, Team, Resource, Wallet, Score
│   │   ├── two-truths.ts
│   │   ├── egg-drop.ts
│   │   └── improv.ts
│   ├── proxy.ts                        # auth middleware
│   └── styles/
│       └── tokens.css                  # brand variables matching prototype
├── public/
│   ├── games-data.json                 # the 215-game catalog (built from master HTML)
│   └── logo.png
├── supabase/
│   ├── migrations/
│   │   ├── 20260601000000_init_core.sql
│   │   ├── 20260601000100_init_rls.sql
│   │   ├── 20260601000200_two_truths.sql
│   │   ├── 20260601000300_egg_drop.sql
│   │   ├── 20260601000400_improv.sql
│   │   ├── 20260601000500_rpcs.sql
│   │   └── 20260601000600_realtime.sql
│   ├── functions/
│   │   ├── send-join-code-email/       # invoke after team creation
│   │   ├── send-debrief-email/         # 1h post-event cron
│   │   └── send-reminder-email/        # 14-day reinforcement
│   ├── seed.sql                         # demo orgs/users/events for staging
│   └── config.toml
├── tests/
│   ├── unit/
│   │   └── lib/                         # join-code, jwt, scoring utils
│   ├── components/
│   │   └── …                            # RTL snapshots + interactions
│   └── e2e/
│       ├── auth.spec.ts
│       ├── two-truths-happy-path.spec.ts
│       ├── egg-drop-happy-path.spec.ts
│       └── improv-happy-path.spec.ts
├── .env.local.example
├── components.json                       # shadcn config
├── eslint.config.mjs
├── next.config.ts
├── package.json
├── postcss.config.mjs
├── tsconfig.json
└── vitest.config.ts
```

## Database schema (concrete DDL to ship)

### Migration 1 — core (shared across games)

```sql
create schema if not exists engage;
create extension if not exists "uuid-ossp";

create table engage.orgs (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  slug text unique not null,
  plan text not null default 'pilot',
  created_at timestamptz default now()
);

create table engage.users (
  id uuid primary key references auth.users(id),
  org_id uuid not null references engage.orgs(id) on delete cascade,
  email text not null,
  display_name text,
  role text not null default 'facilitator',
  created_at timestamptz default now()
);

create table engage.events (
  id uuid primary key default uuid_generate_v4(),
  org_id uuid not null references engage.orgs(id) on delete cascade,
  created_by uuid not null references engage.users(id),
  game_slug text not null check (game_slug in ('two-truths-and-a-lie','egg-drop','improv-challenge')),
  name text not null,
  venue text,
  scheduled_at timestamptz,
  current_phase text not null default 'setup',
  language text not null default 'en',
  config jsonb not null default '{}',
  timer_duration_minutes int default 30,
  timer_started_at timestamptz,
  timer_ends_at timestamptz,
  status text not null default 'draft',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table engage.collaborators (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  user_id uuid references auth.users(id),
  email text not null,
  role text not null check (role in ('admin','judge')),
  created_at timestamptz default now(),
  unique(event_id, email)
);

create table engage.teams (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  name text not null,
  color text,
  avatar text,
  join_code text unique,
  budget_accepted_at timestamptz,
  score int not null default 0,
  coins int not null default 50,
  status text not null default 'active',
  metadata jsonb not null default '{}',
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique(event_id, name)
);

create table engage.team_members (
  id uuid primary key default uuid_generate_v4(),
  team_id uuid not null references engage.teams(id) on delete cascade,
  display_name text not null,
  role text default 'member',
  email text,
  avatar_url text,
  joined_at timestamptz default now()
);

create table engage.audit_log (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid references engage.events(id) on delete set null,
  actor uuid,
  action text not null,
  details jsonb not null default '{}',
  created_at timestamptz default now()
);

create table engage.badges (
  id uuid primary key default uuid_generate_v4(),
  team_id uuid not null references engage.teams(id) on delete cascade,
  badge_id text not null,
  awarded_at timestamptz default now(),
  unique(team_id, badge_id)
);

create table engage.templates (
  id uuid primary key default uuid_generate_v4(),
  org_id uuid not null references engage.orgs(id) on delete cascade,
  created_by uuid not null references engage.users(id),
  game_slug text not null,
  name text not null,
  config jsonb not null default '{}',
  created_at timestamptz default now()
);

-- updated_at trigger
create or replace function engage.touch_updated_at() returns trigger as $$
begin new.updated_at = now(); return new; end;
$$ language plpgsql;

create trigger touch_events before update on engage.events for each row execute procedure engage.touch_updated_at();
create trigger touch_teams before update on engage.teams for each row execute procedure engage.touch_updated_at();
```

### Migration 2 — Two Truths and a Lie

```sql
create schema if not exists two_truths;

create table two_truths.statements (
  id uuid primary key default uuid_generate_v4(),
  team_id uuid not null references engage.teams(id) on delete cascade,
  position int not null check (position in (0,1,2,3)),  -- supports 4th-statement twist
  text text not null,
  is_lie boolean not null default false,
  created_at timestamptz default now(),
  unique(team_id, position)
);

create table two_truths.rounds (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  round_no int not null,
  speaker_team uuid not null references engage.teams(id) on delete cascade,
  shuffled_order jsonb not null,  -- [{position, text}, …] in display order
  lie_display_index int not null,
  twist text,
  started_at timestamptz default now(),
  ended_at timestamptz,
  unique(event_id, round_no)
);

create table two_truths.votes (
  id uuid primary key default uuid_generate_v4(),
  round_id uuid not null references two_truths.rounds(id) on delete cascade,
  voter_team uuid not null references engage.teams(id) on delete cascade,
  choice int not null,
  cast_at timestamptz default now(),
  unique(round_id, voter_team)
);

create table two_truths.scores (
  id uuid primary key default uuid_generate_v4(),
  round_id uuid not null references two_truths.rounds(id) on delete cascade,
  team_id uuid not null references engage.teams(id) on delete cascade,
  delta int not null,
  reason text not null,  -- 'caught_lie' | 'fooled_voter' | 'perfect_lie' | 'twist_bonus'
  created_at timestamptz default now()
);
```

### Migration 3 — Egg Drop (your prototype's rules, NOT eggdrop production)

```sql
create schema if not exists egg_drop;

create table egg_drop.materials (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  slug text not null,             -- 'straws', 'tape', 'cotton', etc. — matches prototype
  name text not null,
  icon text,
  role text not null,             -- 'cushion', 'structure', 'drag', 'utility'
  cost int not null,
  cushion int not null default 0,
  structure int not null default 0,
  drag int not null default 0,
  weight int not null default 0,
  unique(event_id, slug)
);

create table egg_drop.builds (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  team_id uuid not null references engage.teams(id) on delete cascade,
  round_no int not null,
  materials jsonb not null default '[]',  -- [{materialId, qty, position}]
  strategy text,
  budget_used int not null default 0,
  submitted_at timestamptz,
  unique(event_id, team_id, round_no)
);

create table egg_drop.drops (
  id uuid primary key default uuid_generate_v4(),
  build_id uuid not null references egg_drop.builds(id) on delete cascade,
  difficulty int not null,         -- 55 (desk), 78 (balcony), 105 (building)
  event_modifier jsonb,            -- {drag: 1.35} etc.
  survived boolean not null,
  score int not null,
  ran_at timestamptz default now()
);
```

### Migration 4 — Improv Challenge

```sql
create schema if not exists improv;

create table improv.prompts (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  text text not null,
  language text not null default 'en',
  category text,
  difficulty text default 'medium',
  custom boolean not null default false,
  created_at timestamptz default now()
);

create table improv.rounds (
  id uuid primary key default uuid_generate_v4(),
  event_id uuid not null references engage.events(id) on delete cascade,
  round_no int not null,
  team_id uuid not null references engage.teams(id) on delete cascade,
  prompt_id uuid references improv.prompts(id),
  response text,
  twist text,
  started_at timestamptz default now(),
  ended_at timestamptz,
  unique(event_id, round_no)
);

create table improv.criterion_scores (
  id uuid primary key default uuid_generate_v4(),
  round_id uuid not null references improv.rounds(id) on delete cascade,
  team_id uuid not null references engage.teams(id) on delete cascade,
  confidence int check (confidence between 0 and 10),
  storytelling int check (storytelling between 0 and 10),
  audience_connection int check (audience_connection between 0 and 10),
  solution_quality int check (solution_quality between 0 and 10),
  notes text,
  scored_at timestamptz default now()
);
```

### Migration 5 — RLS

```sql
-- Helper
create or replace function engage.is_collaborator(p_event_id uuid, p_role text default null)
returns boolean as $$
begin
  if p_role is null then
    return exists(select 1 from engage.collaborators where event_id=p_event_id and user_id=auth.uid());
  end if;
  return exists(select 1 from engage.collaborators where event_id=p_event_id and user_id=auth.uid() and role=p_role);
end;
$$ language plpgsql security definer;

-- Enable RLS on every table
alter table engage.events enable row level security;
alter table engage.teams enable row level security;
alter table engage.team_members enable row level security;
alter table engage.collaborators enable row level security;
alter table engage.audit_log enable row level security;
alter table engage.badges enable row level security;
alter table engage.templates enable row level security;
alter table two_truths.statements enable row level security;
alter table two_truths.rounds enable row level security;
alter table two_truths.votes enable row level security;
alter table two_truths.scores enable row level security;
alter table egg_drop.materials enable row level security;
alter table egg_drop.builds enable row level security;
alter table egg_drop.drops enable row level security;
alter table improv.prompts enable row level security;
alter table improv.rounds enable row level security;
alter table improv.criterion_scores enable row level security;

-- Policies (pattern: collaborator-gated writes, open-read for live projector)
create policy "Admins manage events" on engage.events for all using (engage.is_collaborator(id, 'admin'));
create policy "Read events" on engage.events for select using (true);
-- … repeat the open-read + collaborator-write pattern for every table …
-- Audit log: only admins can read
create policy "Admins read audit" on engage.audit_log for select using (engage.is_collaborator(event_id, 'admin'));
create policy "System writes audit" on engage.audit_log for insert with check (true);
-- two_truths.statements: hidden from non-collaborators until reveal
create policy "Collaborators read statements" on two_truths.statements for select using (engage.is_collaborator((select event_id from engage.teams where id = team_id)));
create policy "Players read shuffled statements via round" on two_truths.statements for select using (true);  -- shuffled_order column on rounds is the public view
```

### Migration 6 — RPCs

```sql
-- Phase state machine
create or replace function engage.transition_event_phase(p_event_id uuid, p_new_phase text)
returns jsonb language plpgsql security definer as $$
declare v_current text; v_valid_transitions jsonb;
begin
  select current_phase into v_current from engage.events where id = p_event_id;
  if v_current is null then return jsonb_build_object('error','event_not_found'); end if;
  -- validate (table of allowed transitions per game)
  -- if BUILD entered, set timer_started_at + timer_ends_at
  update engage.events set current_phase = p_new_phase, updated_at = now() where id = p_event_id;
  insert into engage.audit_log(event_id, actor, action, details) values (p_event_id, auth.uid(), 'phase_transition', jsonb_build_object('from',v_current,'to',p_new_phase));
  return jsonb_build_object('ok', true);
end; $$;

-- Generate unique join code (32-char alphabet, retries 10x)
create or replace function engage.generate_join_code() returns text language plpgsql as $$
declare v_alphabet text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; v_code text; v_attempt int := 0;
begin
  loop
    v_code := '';
    for i in 1..6 loop v_code := v_code || substr(v_alphabet, 1+floor(random()*32)::int, 1); end loop;
    if not exists(select 1 from engage.teams where join_code = v_code) then return v_code; end if;
    v_attempt := v_attempt + 1;
    if v_attempt > 10 then raise exception 'could not generate unique join code'; end if;
  end loop;
end; $$;

-- Two Truths reveal (server-authoritative scoring)
create or replace function two_truths.reveal_round(p_round_id uuid)
returns table(team_id uuid, delta int, reason text) language plpgsql security definer as $$
declare v_lie int; v_speaker uuid; v_event uuid; v_twist text; v_mult int := 1;
begin
  select lie_display_index, speaker_team, event_id, twist into v_lie, v_speaker, v_event, v_twist from two_truths.rounds where id = p_round_id;
  if v_twist = 'double' then v_mult := 2; end if;
  -- award caught voters
  insert into two_truths.scores(round_id, team_id, delta, reason)
    select p_round_id, voter_team, 10*v_mult, 'caught_lie' from two_truths.votes
    where round_id = p_round_id and choice = v_lie;
  -- award speaker per fooled voter
  insert into two_truths.scores(round_id, team_id, delta, reason)
    values (p_round_id, v_speaker, 5*v_mult * (select count(*) from two_truths.votes where round_id=p_round_id and choice<>v_lie), 'fooled');
  -- update team running totals
  update engage.teams t set score = t.score + s.delta from two_truths.scores s where s.round_id = p_round_id and s.team_id = t.id;
  update two_truths.rounds set ended_at = now() where id = p_round_id;
  insert into engage.audit_log(event_id, actor, action, details) values (v_event, auth.uid(), 'two_truths_reveal', jsonb_build_object('round',p_round_id,'lie',v_lie));
  return query select s.team_id, s.delta, s.reason from two_truths.scores s where s.round_id = p_round_id;
end; $$;

-- Egg Drop drop test + score (uses prototype's formula, not eggdrop production)
create or replace function egg_drop.run_drop(p_build_id uuid, p_event_modifier jsonb default '{}')
returns jsonb language plpgsql security definer as $$
-- compute survival from materials + difficulty + event_modifier
-- insert into egg_drop.drops, update teams.score, write audit
$$;

-- Improv score round
create or replace function improv.score_round(p_round_id uuid, p_confidence int, p_storytelling int, p_audience int, p_solution int, p_notes text)
returns jsonb language plpgsql security definer as $$
-- insert criterion_scores, sum to round total, update teams.score
$$;
```

### Migration 7 — Realtime publication

```sql
alter publication supabase_realtime add table engage.events;
alter publication supabase_realtime add table engage.teams;
alter publication supabase_realtime add table engage.audit_log;
alter publication supabase_realtime add table two_truths.rounds;
alter publication supabase_realtime add table two_truths.votes;
alter publication supabase_realtime add table egg_drop.drops;
alter publication supabase_realtime add table improv.criterion_scores;
```

## Auth flows

- `/login` — Supabase Auth email + password (admin/collab). Email OTP as alt via `signInWithOtp({email, options:{shouldCreateUser:false}})`.
- `/auth/callback` — handles OAuth/magic link callback.
- `/forgot-password` — `supabase.auth.resetPasswordForEmail()`.
- `/team/join?code=ABC123` — validates code via RPC, mints signed JWT `team_session` cookie `{teamId, eventId, exp}`, redirects to `/team`.
- `proxy.ts` middleware:
  - `/admin/*` + `/judge/*` → `auth.getUser()` required → redirect `/login`
  - `/team/*` → `team_session` cookie required → redirect `/team/join`
  - JWT verified via HS256 with `TEAM_SESSION_SECRET`

## Realtime hooks

Pattern: `useEvent(eventId)` subscribes to `postgres_changes` on `engage.events` filtered by row, hydrates from initial SSR fetch. Same shape for `useTeams`, `useWallet`, `useScores`, `useAuditLog`. Three Supabase Realtime channels per event:
- `event:<id>:public` — players + projector
- `event:<id>:team:<tid>` — that team's devices only
- `event:<id>:admin` — collaborators (RLS-gated)

## Email infrastructure

Provider: **Resend** (3000/month free, $20/mo Pro).

Templates (in `supabase/functions/`):
1. `send-join-code-email` — fires after `createTeam()` when captain email is set. Body: code, event name, deep link `/team/join?code=XXX`.
2. `send-debrief-email` — cron 1h post-event, attaches PDF debrief link.
3. `send-reminder-email` — cron 14 days post-event, reinforcement nudge.

Fallback: Supabase Auth's built-in email for OTP/reset (uses Supabase's SMTP).

## Server actions cheat sheet

| Action | RPC called | Audit action |
|---|---|---|
| `createEvent(input)` | direct insert | `event_created` |
| `transitionPhase(eventId, phase)` | `engage.transition_event_phase` | `phase_transition` |
| `createTeam(input)` | direct insert + `engage.generate_join_code` | `team_created` |
| `acceptBudget(teamId)` | direct update + maybeAdvanceFromBudgetOffer | `budget_accepted` |
| `purchaseResource(teamId, resourceId, qty)` (egg drop) | game-specific RPC | `purchase` |
| `castVote(roundId, choice)` (two truths) | direct insert | `vote_cast` |
| `revealRound(roundId)` (two truths) | `two_truths.reveal_round` | `two_truths_reveal` |
| `runDrop(buildId)` (egg drop) | `egg_drop.run_drop` | `drop_test` |
| `scoreRound(roundId, criterion_scores)` (improv) | `improv.score_round` | `improv_scored` |
| `uploadAvatar(file)` | Supabase Storage `avatars` bucket | `avatar_uploaded` |

## Game-specific component checklist

### Two Truths (smallest, port first)
- `private-editor.tsx` — 3 inputs + lie radio, gated to current speaker
- `statement-card.tsx` — display + vote, animated reveal
- `voter-queue.tsx` — chips, auto-advance
- `judge-gate.tsx` — confirm modal + auto-lock on leave
- `power-up-shop.tsx` — 5 items, RPC purchase
- 10 plot twists triggered via admin action
- 10 badges computed at game end

### Egg Drop (heaviest)
- `drop-zone.tsx` — drag-and-drop using `react-dnd` or HTML5 dnd
- `material-card.tsx` — draggable, role-colored
- `marketplace.tsx` — filter by role, preset buttons
- `drop-test-form.tsx` — judge rubric (egg/shield/innovation/presentation)
- `event-card.tsx` — 6 random events
- 3 drop heights, animated drop
- 10 badges

### Improv
- `prompt-card.tsx` — current prompt with shuffle
- `score-dots.tsx` — 4 × 10-dot criterion scoring
- `coaching-tip.tsx` — auto-generated from criterion gaps
- `prompt-creator.tsx` — custom prompts with import/export
- 28 EN prompts + 13 language packs (loaded from `improv.prompts` seeded at event create)
- Radar chart (recharts) for criterion analytics
- 10 badges

## Testing strategy

- **Unit (Vitest):** join-code alphabet, JWT signing/verifying, phase-transition validation, scoring math
- **Component (RTL):** every interactive component renders + responds to clicks/keys
- **E2E (Playwright):** one happy-path per game (login → create event → add 2 teams → run → reveal → leaderboard correct)
- Coverage target: 70%+ on `src/lib/` and `src/app/actions/`, no target on UI

## Deployment

1. Create Vercel project, link GitHub repo, build command `npm run build`, output `.next`
2. Create Supabase project (Pro plan recommended for backups + 2x faster auth)
3. Apply migrations: `supabase db push` from `supabase/migrations/`
4. Deploy Edge Functions: `supabase functions deploy send-join-code-email`
5. Set env vars in Vercel dashboard
6. Custom domain: `engage.edstellar.com` → CNAME to Vercel
7. Preview deploys on every PR, prod deploys on main merge

## Observability

- **Sentry:** initialized in `src/instrumentation.ts`, source maps uploaded on build, breadcrumbs include `event_id` + `team_id`
- **Vercel Analytics:** page views, web vitals
- **Supabase Dashboard:** DB query stats, auth log, function invocations

## CI

`.github/workflows/ci.yml`:
- Trigger: PR + push to main
- Steps: install → `tsc --noEmit` → `eslint` → `vitest run` → `playwright test --project=chromium` → `next build`
- Required to merge

## Phased timeline

| Week | Phase | Deliverable |
|---|---|---|
| 1 | Scaffold + Supabase | Next.js boots, auth login works, schema applies cleanly, three clients separated |
| 2 | Game Loop MVP (Two Truths) | One full game end-to-end manual, audit log writes, no realtime yet |
| 3 | Realtime + Projector | Multi-device sync via Supabase Realtime, `/admin/events/[id]/live` projector view |
| 4 | Admin + Judge + RLS hardening | Events CRUD, teams wizard, resources, judge gate, signed JWT cookies, rate limits |
| 5 | Egg Drop + Improv migrations | All three games on the new stack |
| 6 | Marketing + Email + Debrief + Sentry + CI | Full launch surface, paying-customer-ready |

## Out of scope (don't build now)

- Native mobile apps (web-responsive only)
- Multi-tenant org switching UI (single-active-event model)
- AI-judged scoring
- i18n beyond the 14 game languages
- Payment/billing (manual invoicing for pilot)

## When you say "go"

I'll start with **Week 1, Day 1**: run `create-next-app`, scaffold the directory structure above, paste in the migration SQL files, wire the three Supabase clients, and ship a minimal `/login` that signs in via Supabase Auth. End-of-day target: `npm run dev` boots, login form authenticates against your Supabase project, redirects to a placeholder `/admin`.

I'll commit at every milestone so we can roll back if the direction needs adjusting. The prototype in `engage-prototype/` stays untouched the entire time.
