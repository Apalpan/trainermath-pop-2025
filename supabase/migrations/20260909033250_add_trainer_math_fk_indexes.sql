-- Cover foreign keys reported by Supabase's performance advisor.
create index if not exists tm_attempts_owner_session_idx on public.tm_attempts (owner_id, client_session_id);
create index if not exists tm_recommendations_owner_idx on public.tm_recommendations (owner_id);
create index if not exists tm_sheet_outbox_owner_idx on public.tm_sheet_outbox (owner_id);
