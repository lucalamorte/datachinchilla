-- ============================================================
--  DataChinchilla + Interview Prep · TODO en uno
--
--  Pegá esto entero en el SQL Editor de Supabase y dale Run.
--  Proyecto: sscfykrodjnfnnbmkopp (org snowflakeguide)
--
--  Junta las cinco migraciones en orden. Es seguro correrlo de
--  nuevo: usa IF NOT EXISTS y CREATE OR REPLACE, no borra datos
--  y no toca ninguna otra tabla del proyecto.
-- ============================================================


-- ------------------------------------------------------------
--  01 · la tabla
-- ------------------------------------------------------------
create table if not exists public.snowpath_progress (
  user_id    uuid primary key references auth.users on delete cascade,
  name       text        not null default '',
  done       jsonb       not null default '{}'::jsonb,
  quiz       jsonb       not null default '{}'::jsonb,
  done_at    timestamptz,
  updated_at timestamptz not null default now()
);

-- "create table if not exists" no toca una tabla que ya exista, ni
-- siquiera si le faltan columnas. Si quedó a medias de un intento
-- anterior, esto la completa sin pisar lo que ya tenga adentro.
alter table public.snowpath_progress
  add column if not exists name       text        not null default '',
  add column if not exists done       jsonb       not null default '{}'::jsonb,
  add column if not exists quiz       jsonb       not null default '{}'::jsonb,
  add column if not exists done_at    timestamptz,
  add column if not exists updated_at timestamptz not null default now();

comment on table public.snowpath_progress is
  'Avance de las rutas y del Interview Prep. Una fila por persona. Cada app lee y escribe solo la fila propia.';

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


-- ------------------------------------------------------------
--  02 · de dónde viene cada cuenta
-- ------------------------------------------------------------
alter table public.snowpath_progress
  add column if not exists origin_app text not null default 'snowpath',
  add column if not exists account_created_here boolean not null default false,
  add column if not exists first_seen_at timestamptz not null default now();

comment on column public.snowpath_progress.origin_app is
  'Qué app escribió esta fila por primera vez.';
comment on column public.snowpath_progress.account_created_here is
  'true si la cuenta de auth nació entrando por acá, false si ya existía en el proyecto.';
comment on column public.snowpath_progress.first_seen_at is
  'Primera vez que esta persona entró.';

create index if not exists snowpath_origin_idx
  on public.snowpath_progress (origin_app, account_created_here);

-- El origen lo decide la base, no el navegador. security definer
-- porque auth.users no es legible para el rol authenticated: la
-- función lee una sola columna y no devuelve datos de nadie más.
create or replace function public.snowpath_stamp_origin()
returns trigger
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  meta_app text;
begin
  select raw_user_meta_data->>'app' into meta_app
  from auth.users
  where id = new.user_id;

  new.origin_app := 'snowpath';
  new.account_created_here := coalesce(meta_app = 'snowpath', false);
  new.first_seen_at := now();
  return new;
end;
$$;

revoke all on function public.snowpath_stamp_origin() from public, anon, authenticated;

drop trigger if exists snowpath_stamp_origin_on_insert on public.snowpath_progress;

create trigger snowpath_stamp_origin_on_insert
  before insert on public.snowpath_progress
  for each row execute function public.snowpath_stamp_origin();


-- ------------------------------------------------------------
--  03 · ruta de Data Engineer
-- ------------------------------------------------------------
alter table public.snowpath_progress
  add column if not exists de jsonb not null default '{}'::jsonb;

comment on column public.snowpath_progress.de is
  'Avance de la ruta de Data Engineer: { done: {hito: true}, days: {"2026-08-27": true} }.';


-- ------------------------------------------------------------
--  04 · la ruta que arma cada persona
-- ------------------------------------------------------------
alter table public.snowpath_progress
  add column if not exists custom jsonb not null default '{}'::jsonb;

comment on column public.snowpath_progress.custom is
  'Ruta a medida: { items: ["snowpro:n01","cs50:c03"], done: {id: true}, name: "...", updated: ISO8601 }.
   items es una lista ORDENADA: al sincronizar gana la que tenga updated más nuevo,
   mientras que done se une entre dispositivos.';


-- ------------------------------------------------------------
--  05 · Interview Prep
-- ------------------------------------------------------------
alter table public.snowpath_progress
  add column if not exists gym jsonb not null default '{}'::jsonb;

comment on column public.snowpath_progress.gym is
  'Avance del Interview Prep: { rol, meta, diagHecho, sesiones,
   q: {pregunta: {vistas, aciertos, fallos, estado, ultima, proxima}},
   dias: {"2026-08-31": true} }.
   Al sincronizar, cada pregunta se queda con el lado de "ultima" más
   reciente: sumar los contadores duplicaría en cada sincronización.';


-- ------------------------------------------------------------
--  Permisos, al final y todos juntos
--
--  Un permiso a nivel tabla cubre todas las columnas, y revocar
--  una columna suelta después no lo achica. Por eso se saca el
--  permiso entero y se vuelve a dar columna por columna: las tres
--  del bloque 02 las escribe el trigger, nunca el cliente.
-- ------------------------------------------------------------
revoke insert, update on public.snowpath_progress from authenticated;

grant select on public.snowpath_progress to authenticated;

grant insert (user_id, name, done, quiz, done_at, de, custom, gym)
  on public.snowpath_progress to authenticated;

grant update (name, done, quiz, done_at, de, custom, gym)
  on public.snowpath_progress to authenticated;


-- ============================================================
--  Chequeo: las dos consultas de abajo tienen que devolver algo
-- ============================================================
select relname, relrowsecurity as rls_activa
from pg_class where relname = 'snowpath_progress';

select column_name, data_type
from information_schema.columns
where table_schema = 'public' and table_name = 'snowpath_progress'
order by ordinal_position;

-- Tiene que haber una PRIMARY KEY sobre user_id y una FOREIGN KEY.
-- Sin la primary key el guardado no funciona: el upsert necesita saber
-- cuál es la fila que ya existe para actualizarla en vez de duplicarla.
select tc.constraint_type, kcu.column_name
from information_schema.table_constraints tc
join information_schema.key_column_usage kcu
  on kcu.constraint_name = tc.constraint_name
 and kcu.table_schema = tc.table_schema
where tc.table_schema = 'public'
  and tc.table_name = 'snowpath_progress'
  and tc.constraint_type in ('PRIMARY KEY', 'FOREIGN KEY');
