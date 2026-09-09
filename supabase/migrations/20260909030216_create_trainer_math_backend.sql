-- TrainerMath v4: isolated persistence for Brenda Sofía. Existing tl_* tables are untouched.
create table if not exists public.tm_profiles (
  owner_id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null default 'Brenda Sofía' check (char_length(display_name) between 1 and 80),
  timezone text not null default 'America/Lima' check (char_length(timezone) between 1 and 80),
  app_version text not null default '4.0.0',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.tm_user_state (
  owner_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null default '{}'::jsonb check (jsonb_typeof(state) = 'object'),
  client_revision bigint not null default 0 check (client_revision >= 0),
  updated_at timestamptz not null default now()
);

create table if not exists public.tm_sessions (
  id bigint generated always as identity primary key,
  owner_id uuid not null references auth.users(id) on delete cascade,
  client_session_id text not null check (char_length(client_session_id) between 4 and 80),
  mode text not null check (mode in ('practice','exam')),
  variant text not null default 'variety' check (char_length(variant) between 1 and 30),
  question_count smallint not null check (question_count between 0 and 50),
  correct_count smallint not null check (correct_count between 0 and question_count),
  seconds numeric(10,2) not null default 0 check (seconds between 0 and 86400),
  question_ids jsonb not null default '[]'::jsonb check (jsonb_typeof(question_ids) = 'array'),
  content_version text not null,
  app_version text not null,
  finished_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (owner_id, client_session_id)
);

create table if not exists public.tm_attempts (
  id bigint generated always as identity primary key,
  owner_id uuid not null references auth.users(id) on delete cascade,
  client_attempt_key text not null check (char_length(client_attempt_key) between 4 and 140),
  client_session_id text not null check (char_length(client_session_id) between 4 and 80),
  question_id text not null check (char_length(question_id) between 1 and 80),
  area text not null check (char_length(area) between 1 and 90),
  unit_id text not null check (char_length(unit_id) between 1 and 40),
  unit_label text not null check (char_length(unit_label) between 1 and 140),
  family text not null check (char_length(family) between 1 and 100),
  difficulty smallint not null check (difficulty between 1 and 3),
  correct boolean not null,
  seconds numeric(10,2) not null check (seconds between 0 and 86400),
  target_seconds numeric(10,2) not null check (target_seconds between 1 and 86400),
  assisted boolean not null default false,
  confidence text not null default '' check (confidence in ('','segura','duda','azar')),
  error_reason text not null default '' check (error_reason in ('','concepto','calculo','lectura','tiempo')),
  skipped boolean not null default false,
  attempted_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (owner_id, client_attempt_key),
  foreign key (owner_id, client_session_id) references public.tm_sessions(owner_id, client_session_id) on delete cascade
);

create table if not exists public.tm_skill_states (
  owner_id uuid not null references auth.users(id) on delete cascade,
  unit_id text not null,
  unit_label text not null,
  area text not null,
  attempts integer not null default 0 check (attempts >= 0),
  correct_unassisted integer not null default 0 check (correct_unassisted >= 0),
  within_target integer not null default 0 check (within_target >= 0),
  assisted integer not null default 0 check (assisted >= 0),
  accuracy numeric(6,5) not null default 0 check (accuracy between 0 and 1),
  speed_rate numeric(6,5) not null default 0 check (speed_rate between 0 and 1),
  status text not null default 'nuevo' check (status in ('nuevo','señal inicial','en desarrollo','estable','a velocidad')),
  next_review_at timestamptz,
  algorithm_version text not null default 'adaptive-v1',
  updated_at timestamptz not null default now(),
  primary key (owner_id, unit_id)
);

create table if not exists public.tm_recommendations (
  id bigint generated always as identity primary key,
  owner_id uuid not null references auth.users(id) on delete cascade,
  unit_id text,
  area text,
  reason text not null check (char_length(reason) between 1 and 400),
  payload jsonb not null default '{}'::jsonb check (jsonb_typeof(payload) = 'object'),
  algorithm_version text not null default 'adaptive-v1',
  created_at timestamptz not null default now()
);

create table if not exists public.tm_assistant_events (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  client_event_id uuid not null,
  client_session_id text,
  question_id text,
  intent text not null check (intent in ('explain','strategy','summary')),
  request_summary jsonb not null default '{}'::jsonb check (jsonb_typeof(request_summary) = 'object'),
  response_payload jsonb not null default '{}'::jsonb check (jsonb_typeof(response_payload) = 'object'),
  source text not null check (source in ('catalog','openai','gemini','deterministic_fallback')),
  model text,
  latency_ms integer check (latency_ms between 0 and 120000),
  input_tokens integer check (input_tokens is null or input_tokens >= 0),
  output_tokens integer check (output_tokens is null or output_tokens >= 0),
  created_at timestamptz not null default now(),
  unique (owner_id, client_event_id)
);

create table if not exists public.tm_sheet_outbox (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  event_key text not null check (char_length(event_key) between 4 and 180),
  event_type text not null check (event_type in ('session','release')),
  payload jsonb not null check (jsonb_typeof(payload) = 'object'),
  status text not null default 'pending' check (status in ('pending','processing','sent','failed')),
  attempts smallint not null default 0 check (attempts between 0 and 20),
  last_error text,
  next_attempt_at timestamptz not null default now(),
  sent_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (event_key)
);

create index if not exists tm_attempts_owner_time_idx on public.tm_attempts (owner_id, attempted_at desc);
create index if not exists tm_attempts_owner_unit_idx on public.tm_attempts (owner_id, unit_id, attempted_at desc);
create index if not exists tm_sessions_owner_time_idx on public.tm_sessions (owner_id, finished_at desc);
create index if not exists tm_assistant_owner_time_idx on public.tm_assistant_events (owner_id, created_at desc);
create index if not exists tm_sheet_outbox_pending_idx on public.tm_sheet_outbox (status, next_attempt_at) where status in ('pending','failed');

create or replace function public.tm_set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists tm_profiles_updated_at on public.tm_profiles;
create trigger tm_profiles_updated_at before update on public.tm_profiles for each row execute function public.tm_set_updated_at();
drop trigger if exists tm_user_state_updated_at on public.tm_user_state;
create trigger tm_user_state_updated_at before update on public.tm_user_state for each row execute function public.tm_set_updated_at();
drop trigger if exists tm_skill_states_updated_at on public.tm_skill_states;
create trigger tm_skill_states_updated_at before update on public.tm_skill_states for each row execute function public.tm_set_updated_at();
drop trigger if exists tm_sheet_outbox_updated_at on public.tm_sheet_outbox;
create trigger tm_sheet_outbox_updated_at before update on public.tm_sheet_outbox for each row execute function public.tm_set_updated_at();

alter table public.tm_profiles enable row level security;
alter table public.tm_user_state enable row level security;
alter table public.tm_sessions enable row level security;
alter table public.tm_attempts enable row level security;
alter table public.tm_skill_states enable row level security;
alter table public.tm_recommendations enable row level security;
alter table public.tm_assistant_events enable row level security;
alter table public.tm_sheet_outbox enable row level security;

revoke all on public.tm_profiles, public.tm_user_state, public.tm_sessions, public.tm_attempts, public.tm_skill_states, public.tm_recommendations, public.tm_assistant_events, public.tm_sheet_outbox from anon;
grant select, insert, update on public.tm_profiles, public.tm_user_state to authenticated;
grant select, insert on public.tm_sessions, public.tm_attempts to authenticated;
grant select on public.tm_skill_states, public.tm_recommendations, public.tm_assistant_events, public.tm_sheet_outbox to authenticated;

drop policy if exists tm_profiles_select_own on public.tm_profiles;
create policy tm_profiles_select_own on public.tm_profiles for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_profiles_insert_own on public.tm_profiles;
create policy tm_profiles_insert_own on public.tm_profiles for insert to authenticated with check ((select auth.uid()) = owner_id);
drop policy if exists tm_profiles_update_own on public.tm_profiles;
create policy tm_profiles_update_own on public.tm_profiles for update to authenticated using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);

drop policy if exists tm_user_state_select_own on public.tm_user_state;
create policy tm_user_state_select_own on public.tm_user_state for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_user_state_insert_own on public.tm_user_state;
create policy tm_user_state_insert_own on public.tm_user_state for insert to authenticated with check ((select auth.uid()) = owner_id);
drop policy if exists tm_user_state_update_own on public.tm_user_state;
create policy tm_user_state_update_own on public.tm_user_state for update to authenticated using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);

drop policy if exists tm_sessions_select_own on public.tm_sessions;
create policy tm_sessions_select_own on public.tm_sessions for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_sessions_insert_own on public.tm_sessions;
create policy tm_sessions_insert_own on public.tm_sessions for insert to authenticated with check ((select auth.uid()) = owner_id);

drop policy if exists tm_attempts_select_own on public.tm_attempts;
create policy tm_attempts_select_own on public.tm_attempts for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_attempts_insert_own on public.tm_attempts;
create policy tm_attempts_insert_own on public.tm_attempts for insert to authenticated with check ((select auth.uid()) = owner_id);

drop policy if exists tm_skill_states_select_own on public.tm_skill_states;
create policy tm_skill_states_select_own on public.tm_skill_states for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_recommendations_select_own on public.tm_recommendations;
create policy tm_recommendations_select_own on public.tm_recommendations for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_assistant_events_select_own on public.tm_assistant_events;
create policy tm_assistant_events_select_own on public.tm_assistant_events for select to authenticated using ((select auth.uid()) = owner_id);
drop policy if exists tm_sheet_outbox_select_own on public.tm_sheet_outbox;
create policy tm_sheet_outbox_select_own on public.tm_sheet_outbox for select to authenticated using ((select auth.uid()) = owner_id);

comment on table public.tm_sheet_outbox is 'Idempotent operational mirror queue for the TrainerMath_v4 Google Sheets tab.';
