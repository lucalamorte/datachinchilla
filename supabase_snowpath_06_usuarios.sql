-- ============================================================
--  06 · base de usuarios, consentimiento y uso
--
--  Corré este archivo después de supabase_TODO.sql. Es seguro
--  repetirlo: usa IF NOT EXISTS y CREATE OR REPLACE, y no toca
--  los datos que ya estén cargados.
--
--  Hasta ahora lo único que se guardaba de una persona era su
--  avance. Esto agrega quién es, si acepta que le escribas, y
--  qué hace, que es lo que hace falta para tomar decisiones y
--  para que una app nueva arranque con la gente que ya está.
--
--  Tres tablas y una razón para cada una:
--
--    usuarios         quién es y en qué estado está hoy
--    consentimientos  el historial de cada sí y cada no
--    eventos          qué hizo y cuándo
--
--  El consentimiento va aparte y es solo de agregar. El estado
--  actual se puede leer de usuarios, que es cómodo, pero la
--  prueba de que alguien aceptó, cuándo y desde qué app vive en
--  el historial. Si algún día alguien reclama, un booleano no
--  alcanza: hace falta la fecha.
-- ============================================================


-- ------------------------------------------------------------
--  usuarios · una fila por persona, compartida entre las apps
-- ------------------------------------------------------------
create table if not exists public.usuarios (
  user_id       uuid primary key references auth.users on delete cascade,
  nombre        text        not null default '',
  rol_objetivo  text,                       -- data_engineer, data_analyst, ...
  seniority     text,                       -- estudiante, junior, semi, senior
  plazo         text,                       -- 30, 90, lejos, general
  como_llego    text,                       -- canal por el que llegó, si lo dice
  primera_app   text        not null default 'desconocida',
  ultima_app    text,
  marketing_ok  boolean     not null default false,
  marketing_desde timestamptz,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

comment on table public.usuarios is
  'Perfil compartido por todas las apps del proyecto. Una fila por persona.
   marketing_ok es un espejo del último consentimiento: la fuente de verdad
   es la tabla consentimientos.';

comment on column public.usuarios.primera_app is
  'Qué app la trajo. No se sobrescribe nunca: es el dato de adquisición.';
comment on column public.usuarios.marketing_ok is
  'Lo escribe el trigger desde consentimientos, nunca el cliente.';

alter table public.usuarios enable row level security;

drop policy if exists "usuarios: leer lo propio"     on public.usuarios;
drop policy if exists "usuarios: insertar lo propio" on public.usuarios;
drop policy if exists "usuarios: editar lo propio"   on public.usuarios;

create policy "usuarios: leer lo propio"
  on public.usuarios for select using (auth.uid() = user_id);
create policy "usuarios: insertar lo propio"
  on public.usuarios for insert with check (auth.uid() = user_id);
create policy "usuarios: editar lo propio"
  on public.usuarios for update using (auth.uid() = user_id)
                       with check (auth.uid() = user_id);


-- ------------------------------------------------------------
--  consentimientos · solo se agrega, nunca se edita ni se borra
-- ------------------------------------------------------------
create table if not exists public.consentimientos (
  id         bigint generated always as identity primary key,
  user_id    uuid        not null references auth.users on delete cascade,
  tipo       text        not null default 'marketing',
  valor      boolean     not null,
  app        text        not null default 'desconocida',
  momento    timestamptz not null default now()
);

comment on table public.consentimientos is
  'Historial de cada sí y cada no. Append-only: sin policy de update ni de
   delete, así el registro no se puede reescribir después.';

create index if not exists consentimientos_user_idx
  on public.consentimientos (user_id, tipo, momento desc);

alter table public.consentimientos enable row level security;

drop policy if exists "consent: leer lo propio"     on public.consentimientos;
drop policy if exists "consent: insertar lo propio" on public.consentimientos;

create policy "consent: leer lo propio"
  on public.consentimientos for select using (auth.uid() = user_id);
create policy "consent: insertar lo propio"
  on public.consentimientos for insert with check (auth.uid() = user_id);

-- El estado de usuarios lo decide el historial, no el navegador.
create or replace function public.tocar_consentimiento()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.tipo = 'marketing' then
    update public.usuarios
       set marketing_ok    = new.valor,
           marketing_desde = new.momento,
           updated_at      = now()
     where user_id = new.user_id;
  end if;
  return new;
end;
$$;

revoke all on function public.tocar_consentimiento() from public, anon, authenticated;

drop trigger if exists consentimiento_espejo on public.consentimientos;
create trigger consentimiento_espejo
  after insert on public.consentimientos
  for each row execute function public.tocar_consentimiento();


-- ------------------------------------------------------------
--  eventos · qué hizo y cuándo
--
--  Deliberadamente chico: qué pasó, en qué app, cuándo, y un
--  jsonb para lo que cambie con el tiempo. Nada de datos
--  personales acá adentro: para eso está usuarios.
-- ------------------------------------------------------------
create table if not exists public.eventos (
  id          bigint generated always as identity primary key,
  user_id     uuid        not null references auth.users on delete cascade,
  app         text        not null,
  evento      text        not null,
  props       jsonb       not null default '{}'::jsonb,
  ocurrido_en timestamptz not null default now()
);

comment on table public.eventos is
  'Uso, para retención y decisiones de producto. Sin datos personales:
   el quién es un user_id y el resto vive en usuarios.';

create index if not exists eventos_user_idx on public.eventos (user_id, ocurrido_en desc);
create index if not exists eventos_app_idx  on public.eventos (app, evento, ocurrido_en desc);

alter table public.eventos enable row level security;

drop policy if exists "eventos: leer lo propio"     on public.eventos;
drop policy if exists "eventos: insertar lo propio" on public.eventos;

create policy "eventos: leer lo propio"
  on public.eventos for select using (auth.uid() = user_id);
create policy "eventos: insertar lo propio"
  on public.eventos for insert with check (auth.uid() = user_id);


-- ------------------------------------------------------------
--  updated_at se actualiza solo
-- ------------------------------------------------------------
create or replace function public.usuarios_touch()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists usuarios_touch_updated_at on public.usuarios;
create trigger usuarios_touch_updated_at
  before update on public.usuarios
  for each row execute function public.usuarios_touch();

-- primera_app es el dato de adquisición: se escribe una vez y no se pisa.
create or replace function public.usuarios_fijar_primera_app()
returns trigger language plpgsql as $$
begin
  new.primera_app = old.primera_app;
  new.created_at  = old.created_at;
  return new;
end;
$$;

drop trigger if exists usuarios_primera_app on public.usuarios;
create trigger usuarios_primera_app
  before update on public.usuarios
  for each row execute function public.usuarios_fijar_primera_app();


-- ------------------------------------------------------------
--  PERMISOS
--
--  El cliente escribe lo que la persona declara de sí misma.
--  marketing_ok, primera_app y las fechas las escribe la base.
-- ------------------------------------------------------------
revoke insert, update on public.usuarios from authenticated;

grant select on public.usuarios to authenticated;
grant insert (user_id, nombre, rol_objetivo, seniority, plazo, como_llego,
              primera_app, ultima_app)
  on public.usuarios to authenticated;
grant update (nombre, rol_objetivo, seniority, plazo, como_llego, ultima_app)
  on public.usuarios to authenticated;

grant select, insert on public.consentimientos to authenticated;
grant usage, select on all sequences in schema public to authenticated;

grant select, insert on public.eventos to authenticated;


-- ============================================================
--  VISTAS PARA DECIDIR
--
--  No llevan grant: se consultan desde el SQL Editor, que
--  trabaja con service role. Ninguna queda expuesta al navegador.
-- ============================================================

-- Un día de actividad por persona y por app. Es la base de todo
-- lo demás: retención, frecuencia, días activos.
create or replace view public.vw_actividad_diaria as
select user_id,
       app,
       date_trunc('day', ocurrido_en)::date as dia,
       count(*)                             as eventos
from public.eventos
group by 1, 2, 3;

-- Retención por cohorte de alta. Cada fila dice cuánta gente de la
-- cohorte del mes X seguía activa N días después de darse de alta.
create or replace view public.vw_retencion as
with alta as (
  select user_id,
         date_trunc('month', created_at)::date as cohorte,
         created_at::date                      as dia_alta
  from public.usuarios
)
select a.cohorte,
       (d.dia - a.dia_alta)              as dias_desde_alta,
       count(distinct d.user_id)         as activos,
       (select count(*) from alta a2 where a2.cohorte = a.cohorte) as cohorte_total
from alta a
join public.vw_actividad_diaria d on d.user_id = a.user_id
group by 1, 2;

-- A quién se le puede escribir, con el mail y desde cuándo aceptó.
-- Solo service role: toca auth.users.
create or replace view public.vw_alcanzables as
select u.user_id,
       au.email,
       u.nombre,
       u.rol_objetivo,
       u.primera_app,
       u.marketing_desde,
       u.updated_at
from public.usuarios u
join auth.users au on au.id = u.user_id
where u.marketing_ok;


-- ============================================================
--  CONSULTAS PARA EL DÍA A DÍA
--  (copiá y pegá en el SQL Editor cuando las necesites)
-- ============================================================

-- 1. Cuánta gente hay, cuánta acepta que le escribas, de dónde vino.
--
--    select primera_app,
--           count(*)                                as personas,
--           count(*) filter (where marketing_ok)    as alcanzables,
--           round(100.0 * count(*) filter (where marketing_ok) / count(*), 1) as pct
--    from public.usuarios
--    group by 1 order by personas desc;

-- 2. Retención a 1, 7 y 30 días por cohorte mensual.
--
--    select cohorte,
--           max(cohorte_total) as tamano,
--           max(activos) filter (where dias_desde_alta = 1)  as d1,
--           max(activos) filter (where dias_desde_alta = 7)  as d7,
--           max(activos) filter (where dias_desde_alta = 30) as d30
--    from public.vw_retencion
--    group by 1 order by 1 desc;

-- 3. Gente que usa más de una app. Es el número que dice si la base
--    se puede apalancar o si cada app vive sola.
--
--    select count(*) filter (where apps = 1) as una_sola,
--           count(*) filter (where apps > 1) as varias
--    from (select user_id, count(distinct app) as apps
--          from public.eventos group by 1) t;

-- 4. Qué eventos ocurren más, por app. Sirve para saber qué se usa.
--
--    select app, evento, count(*) as veces,
--           count(distinct user_id) as personas
--    from public.eventos
--    group by 1, 2 order by veces desc limit 30;

-- 5. Los que aceptaron y todavía no recibieron nada, para una campaña.
--
--    select email, nombre, rol_objetivo, marketing_desde
--    from public.vw_alcanzables
--    order by marketing_desde desc;

-- 6. Bajas: quiénes se dieron de baja de los mensajes y cuándo.
--
--    select c.user_id, c.momento, c.app
--    from public.consentimientos c
--    where c.tipo = 'marketing' and not c.valor
--    order by c.momento desc;


-- ============================================================
--  CHEQUEO
-- ============================================================
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in ('usuarios', 'consentimientos', 'eventos')
order by table_name;
