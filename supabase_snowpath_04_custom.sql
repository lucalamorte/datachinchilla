-- ============================================================
--  SnowPro Core Path · 04 · la ruta que arma cada persona
--
--  Corré este archivo después de los tres anteriores. Es seguro
--  repetirlo y no toca los datos que ya estén cargados.
--
--  El armador (armar.html) guarda en la MISMA fila que las otras
--  rutas, en una columna aparte. Una sola fila por persona.
-- ============================================================

alter table public.snowpath_progress
  add column if not exists custom jsonb not null default '{}'::jsonb;

comment on column public.snowpath_progress.custom is
  'Ruta a medida: { items: ["snowpro:n01","cs50:c03"], done: {id: true}, name: "...", updated: ISO8601 }.
   items es una lista ORDENADA: al sincronizar gana la que tenga updated más nuevo,
   mientras que done se une entre dispositivos.';

-- el permiso se da por columna, como las demás que escribe el cliente
grant update (custom) on public.snowpath_progress to authenticated;
grant insert (custom) on public.snowpath_progress to authenticated;

-- ============================================================
--  Para mirar qué arma la gente
-- ============================================================

-- 1. Cuánta gente armó su propia ruta y de cuántos niveles.
--
--    select
--      count(*) filter (where jsonb_array_length(coalesce(custom->'items','[]'::jsonb)) > 0) as con_ruta_propia,
--      round(avg(jsonb_array_length(coalesce(custom->'items','[]'::jsonb)))
--            filter (where jsonb_array_length(coalesce(custom->'items','[]'::jsonb)) > 0), 1) as niveles_promedio
--    from public.snowpath_progress;

-- 2. Qué niveles del catálogo son los más elegidos. Sirve para saber
--    qué material vale la pena ampliar y cuál no lo usa nadie.
--
--    select pieza, count(*) as veces
--    from public.snowpath_progress,
--         lateral jsonb_array_elements_text(coalesce(custom->'items','[]'::jsonb)) as pieza
--    group by pieza
--    order by veces desc;

-- 3. Con qué ruta se quedan más: la armada o las del sitio.
--
--    select
--      count(*) filter (where jsonb_array_length(coalesce(custom->'items','[]'::jsonb)) > 0
--                         and custom->'done' <> '{}'::jsonb) as avanzo_en_la_propia,
--      count(*) filter (where done <> '{}'::jsonb)            as avanzo_en_snowpro,
--      count(*) filter (where de->'done' <> '{}'::jsonb)      as avanzo_en_data_engineer
--    from public.snowpath_progress;
