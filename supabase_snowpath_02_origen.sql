-- ============================================================
--  SnowPro Core Path · 02 · marcar de dónde viene cada cuenta
--
--  Corré este archivo después del primero. Es seguro repetirlo:
--  usa IF NOT EXISTS y CREATE OR REPLACE, y no toca los datos
--  que ya estén cargados.
--
--  Sirve para separar, el día que quieras mover el path a su propio
--  proyecto, las cuentas que nacieron acá de las que ya existían.
-- ============================================================

alter table public.snowpath_progress
  add column if not exists origin_app text not null default 'snowpath',
  add column if not exists account_created_here boolean not null default false,
  add column if not exists first_seen_at timestamptz not null default now();

comment on column public.snowpath_progress.origin_app is
  'Qué app escribió esta fila por primera vez. Hoy siempre snowpath.';
comment on column public.snowpath_progress.account_created_here is
  'true si la cuenta de auth nació entrando al path, false si ya existía en el proyecto.';
comment on column public.snowpath_progress.first_seen_at is
  'Primera vez que esta persona entró al path.';

create index if not exists snowpath_origin_idx
  on public.snowpath_progress (origin_app, account_created_here);

-- ------------------------------------------------------------
--  El origen lo decide la base, no el navegador.
--
--  Cuando alguien entra por primera vez desde esta página, el login
--  guarda app='snowpath' en la metadata de la cuenta. Esa metadata
--  solo se escribe al crear la cuenta, así que distingue con
--  exactitud quién nació acá de quién ya estaba.
--
--  security definer porque auth.users no es legible para el rol
--  authenticated. La función solo lee una columna y no devuelve
--  datos de otras personas.
-- ------------------------------------------------------------
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

-- Las tres columnas las escribe el trigger, nunca el cliente.
--
-- Un permiso a nivel tabla cubre todas las columnas, y revocar una
-- columna suelta despues no lo achica. Por eso se saca el permiso
-- entero y se vuelve a dar columna por columna.
revoke insert, update on public.snowpath_progress from authenticated;

grant select on public.snowpath_progress to authenticated;
grant insert (user_id, name, done, quiz, done_at)
  on public.snowpath_progress to authenticated;
grant update (name, done, quiz, done_at)
  on public.snowpath_progress to authenticated;

-- ============================================================
--  Consultas para el día de la migración
--  (corrélas desde el SQL Editor, que trabaja con service role)
-- ============================================================

-- 1. Cuentas que nacieron en el path. Son las que se pueden mover
--    sin afectar a la otra app.
--
--    select u.id, u.email, u.created_at, p.first_seen_at
--    from auth.users u
--    join public.snowpath_progress p on p.user_id = u.id
--    where p.account_created_here
--    order by p.first_seen_at;

-- 2. Cuántas cuentas del path suman al plan del proyecto.
--
--    select count(*) filter (where account_created_here) as nacidas_aca,
--           count(*)                                     as total_del_path
--    from public.snowpath_progress;

-- 3. Cuentas compartidas con tu otra app. Cambiá TABLA_DE_LA_OTRA_APP
--    por la tabla donde PrimeroLab guarda su user_id.
--
--    select u.email
--    from auth.users u
--    join public.snowpath_progress p   on p.user_id = u.id
--    join public.TABLA_DE_LA_OTRA_APP o on o.user_id = u.id;

-- 4. El origen también queda en la cuenta, aunque alguien borre su
--    fila de progreso.
--
--    select id, email, raw_user_meta_data->>'app' as origen, created_at
--    from auth.users
--    order by created_at desc;
