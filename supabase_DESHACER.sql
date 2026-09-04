-- ============================================================
--  DESHACER · sacar del proyecto equivocado lo que crearon
--  las migraciones de DataChinchilla + Interview Prep.
--
--  Corré esto en el proyecto de la organización "primero"
--  (blalndyyatqodqsdsiji), NO en el nuevo.
--
--  Toca únicamente lo que crearon esas migraciones: la tabla
--  snowpath_progress y sus dos funciones. Las políticas, el
--  índice y los triggers se van solos con la tabla.
--
--  No nombra ni roza nada de PrimeroLab: card_progress y todo
--  lo demás quedan exactamente como están.
-- ============================================================


-- ------------------------------------------------------------
--  PRIMERO MIRAR, DESPUÉS BORRAR
--
--  Corré este bloque solo y leé los dos resultados antes de
--  seguir. Si las dos consultas vienen vacías, el DROP de abajo
--  no le borra el avance a nadie.
-- ------------------------------------------------------------
select count(*) as filas_de_progreso from public.snowpath_progress;

select id, email, created_at, raw_user_meta_data->>'app' as vino_de
from auth.users
where raw_user_meta_data->>'app' in ('snowpath', 'prep')
order by created_at desc;


-- ------------------------------------------------------------
--  BORRAR
--
--  De acá para abajo no hay vuelta atrás. Si la primera consulta
--  devolvió filas, exportalas antes.
-- ------------------------------------------------------------
drop table if exists public.snowpath_progress;

drop function if exists public.snowpath_touch();
drop function if exists public.snowpath_stamp_origin();


-- ------------------------------------------------------------
--  CHEQUEO
--  La primera tiene que devolver 0 filas: ya no queda nada.
--  La segunda tiene que seguir mostrando card_progress y lo
--  demás de PrimeroLab, intacto.
-- ------------------------------------------------------------
select table_name
from information_schema.tables
where table_schema = 'public' and table_name = 'snowpath_progress';

select table_name
from information_schema.tables
where table_schema = 'public'
order by table_name;


-- ============================================================
--  LO QUE ESTO NO BORRA
--
--  Las cuentas de auth.users no se van con la tabla: el borrado
--  va de la fila de progreso hacia la cuenta, nunca al revés.
--  Si la segunda consulta de arriba te mostró cuentas creadas
--  desde estas páginas y no las querés en este proyecto,
--  borralas a mano desde Authentication → Users.
--
--  En el proyecto nuevo hay que correr supabase_TODO.sql, y
--  volver a configurar Site URL y Redirect URLs: eso es por
--  proyecto y no se copia.
-- ============================================================
