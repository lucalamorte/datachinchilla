-- ============================================================
--  05 · avance del Data Interview Gym
--
--  Corré este archivo después de los cuatro anteriores. Es seguro
--  repetirlo y no toca los datos que ya estén cargados.
--
--  El gimnasio guarda en la MISMA fila que las rutas, en una
--  columna aparte. Una sola fila por persona: cuando las dos apps
--  se fusionen, el perfil ya va a ser el mismo.
-- ============================================================

alter table public.snowpath_progress
  add column if not exists gym jsonb not null default '{}'::jsonb;

comment on column public.snowpath_progress.gym is
  'Avance del Data Interview Gym: { meta, diagHecho, sesiones,
   q: {pregunta: {vistas, aciertos, fallos, estado, ultima, proxima}},
   dias: {"2026-08-31": true} }.
   Al sincronizar, cada pregunta se queda con el lado de "ultima" mas
   reciente: sumar los contadores duplicaria en cada sincronizacion.';

-- el permiso se da por columna, como las demás que escribe el cliente
grant update (gym) on public.snowpath_progress to authenticated;
grant insert (gym) on public.snowpath_progress to authenticated;

-- ============================================================
--  Para mirar el uso
-- ============================================================

-- 1. Cuanta gente entro al gimnasio y cuantas sesiones hizo.
--
--    select
--      count(*) filter (where gym->'q' <> '{}'::jsonb)     as con_practica,
--      round(avg((gym->>'sesiones')::int)
--            filter (where gym ? 'sesiones'), 1)           as sesiones_promedio
--    from public.snowpath_progress;

-- 2. La senal que mas importa segun el spec: vuelven a practicar lo
--    que fallaron?
--
--    select count(*) as practicaron_sus_errores
--    from public.snowpath_progress
--    where exists (
--      select 1 from jsonb_each(gym->'q') as t(id, f)
--      where (f->>'fallos')::int > 0 and (f->>'vistas')::int > 1
--    );
