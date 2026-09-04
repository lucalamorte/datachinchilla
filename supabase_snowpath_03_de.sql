-- ============================================================
--  SnowPro Core Path · 03 · avance de la ruta de Data Engineer
--
--  Corré este archivo después de los dos anteriores. Es seguro
--  repetirlo y no toca los datos que ya estén cargados.
--
--  La ruta de Data Engineer guarda su avance en la MISMA fila que
--  el path de SnowPro, en una columna aparte. Una sola fila por
--  persona, dos rutas adentro.
-- ============================================================

alter table public.snowpath_progress
  add column if not exists de jsonb not null default '{}'::jsonb;

comment on column public.snowpath_progress.de is
  'Avance de la ruta de Data Engineer: { done: {hito: true}, days: {"2026-08-27": true} }.';

-- el permiso se da por columna, como las demás que escribe el cliente
grant update (de) on public.snowpath_progress to authenticated;
grant insert (de) on public.snowpath_progress to authenticated;

-- ============================================================
--  Para mirar el uso de cada ruta
-- ============================================================

-- 1. Cuánta gente avanzó en cada una.
--
--    select
--      count(*) filter (where done <> '{}'::jsonb)                as en_snowpro,
--      count(*) filter (where de->'done' <> '{}'::jsonb)          as en_data_engineer,
--      count(*) filter (where done <> '{}'::jsonb
--                         and de->'done' <> '{}'::jsonb)          as en_las_dos
--    from public.snowpath_progress;

-- 2. Quien mas dias de practica acumulo.
--
--    select name,
--           (select count(*) from jsonb_object_keys(de->'days')) as dias_practicados
--    from public.snowpath_progress
--    where de ? 'days'
--    order by dias_practicados desc
--    limit 20;
