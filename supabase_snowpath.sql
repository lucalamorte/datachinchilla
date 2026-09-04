-- ============================================================
--  SnowPro Core Path · progreso en la nube
--  Corré este archivo entero en el SQL Editor de tu proyecto.
--
--  Solo crea la tabla snowpath_progress. No toca ninguna tabla
--  existente, no modifica auth.users y no cambia permisos de
--  otras apps del mismo proyecto.
-- ============================================================

create table if not exists public.snowpath_progress (
  user_id    uuid primary key references auth.users on delete cascade,
  name       text        not null default '',
  done       jsonb       not null default '{}'::jsonb,   -- hitos del mapa
  quiz       jsonb       not null default '{}'::jsonb,   -- preguntas falladas
  done_at    timestamptz,                                -- cuando cerró los 15
  updated_at timestamptz not null default now()
);

comment on table public.snowpath_progress is
  'Avance del path de SnowPro Core. Una fila por persona. La app solo lee y escribe la fila propia.';

-- ------------------------------------------------------------
--  Row Level Security: cada quien ve y escribe únicamente lo suyo
-- ------------------------------------------------------------
alter table public.snowpath_progress enable row level security;

drop policy if exists "snowpath: leer lo propio"     on public.snowpath_progress;
drop policy if exists "snowpath: insertar lo propio" on public.snowpath_progress;
drop policy if exists "snowpath: editar lo propio"   on public.snowpath_progress;

create policy "snowpath: leer lo propio"
  on public.snowpath_progress for select
  using (auth.uid() = user_id);

create policy "snowpath: insertar lo propio"
  on public.snowpath_progress for insert
  with check (auth.uid() = user_id);

create policy "snowpath: editar lo propio"
  on public.snowpath_progress for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- sin policy de delete: la fila se borra sola si se borra la cuenta

grant select, insert, update on public.snowpath_progress to authenticated;

-- ------------------------------------------------------------
--  updated_at se actualiza solo, así el cliente no puede mentir
-- ------------------------------------------------------------
create or replace function public.snowpath_touch()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists snowpath_touch_updated_at on public.snowpath_progress;

create trigger snowpath_touch_updated_at
  before update on public.snowpath_progress
  for each row execute function public.snowpath_touch();

-- ============================================================
--  Chequeo rápido: esto tiene que devolver la tabla con RLS activa
-- ============================================================
-- select relname, relrowsecurity from pg_class where relname = 'snowpath_progress';
