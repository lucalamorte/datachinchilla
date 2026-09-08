# -*- coding: utf-8 -*-
u"""CS50, semana por semana en vez de curso por curso.

   La ruta tenia once pasos y cada paso era un curso entero: CS50x son
   sesenta horas, Games sesenta, Scratch cincuenta. Cuarenta y dos
   horas por paso de promedio.

   El planificador reparte la semana en bloques de noventa minutos,
   asi que un paso de sesenta horas se partia en cuarenta bloques
   iguales. Ya se arreglo que no mintiera con el numero -antes decia
   "parte 1 de 40" todas las semanas-, pero eso lo hizo honesto, no
   util: seguis sin poder marcar nada hecho hasta terminar las sesenta
   horas, y la agenda te repite el mismo renglon dos meses.

   Harvard publica la estructura. No hay que inventarla: CS50x son
   once semanas con nombre propio mas el proyecto final, CS50 Python
   nueve mas proyecto, CS50 SQL siete. Cada una tiene su pagina y su
   problem set. Los titulos de aca salen de esas paginas, comprobados
   uno por uno.

   Se parten esos tres y no los once. Los otros ocho quedan enteros a
   proposito, y se dice en la pagina: CS50x, Python y SQL son los que
   alguien de este sitio hace de punta a punta; Games, Business o Law
   se eligen, no se recorren, y partirlos seria llenar el mapa de
   pasos que nadie va a tocar.

   Los minutos no se re-estiman: se reparten los que la ruta ya tenia.
   Sesenta horas de CS50x entre doce unidades son cinco por unidad.
   Harvard no publica horas por semana, y repartir en partes iguales
   es lo unico que no es inventar.

   Uso: python build-cs50-semanas.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cs50.html")

# --- CS50x: los once semanas y el proyecto, con el titulo que les
#     pone Harvard en su propia pagina.
CS50X = [
 (u"Semana 0 · Scratch", u"weeks/0/",
  u"Programación visual con bloques: bucles, condiciones y variables sin pelear con la sintaxis."),
 (u"Semana 1 · C", u"weeks/1/",
  u"El primer lenguaje de verdad. Compilar, tipos, funciones y por qué C se sigue enseñando primero."),
 (u"Semana 2 · Arrays", u"weeks/2/",
  u"Arreglos, cadenas y argumentos de línea de comandos. Acá aparece la idea de que la memoria es una fila."),
 (u"Semana 3 · Algoritmos", u"weeks/3/",
  u"Búsqueda, ordenamiento y notación asintótica. Es la semana que más se nota en una entrevista."),
 (u"Semana 4 · Memoria", u"weeks/4/",
  u"Punteros, memoria dinámica y archivos. La semana que más gente asusta, y la que más cambia cómo pensás el resto."),
 (u"Semana 5 · Estructuras de datos", u"weeks/5/",
  u"Listas enlazadas, tablas de hash y árboles. Lo que hay debajo de cada estructura que después usás sin mirar."),
 (u"Semana 6 · Python", u"weeks/6/",
  u"El mismo problema en un lenguaje de alto nivel, y por qué se entiende mejor habiendo pasado por C."),
 (u"Semana 7 · SQL", u"weeks/7/",
  u"Guardar datos en una base y consultarlos. Es la puerta a la mitad del catálogo de este sitio."),
 (u"Semana 8 · HTML, CSS y JavaScript", u"weeks/8/",
  u"La web del lado del navegador: estructura, estilo y comportamiento."),
 (u"Semana 9 · Flask", u"weeks/9/",
  u"Del lado del servidor: rutas, plantillas y sesiones, con Python."),
 (u"Semana 10 · El cierre", u"weeks/10/",
  u"La última semana de material antes del proyecto."),
 (u"Proyecto final", u"project/",
  u"Lo que quieras, con lo que aprendiste. Es lo que después mostrás, y lo que hace que el curso se te quede."),
]

# --- CS50 Python: nueve semanas con nombre, mas el proyecto.
CS50P = [
 (u"Semana 0 · Funciones", u"weeks/0/", u"Funciones, argumentos y valores de retorno, desde cero."),
 (u"Semana 1 · Condicionales", u"weeks/1/", u"Decidir: comparaciones, ramas y el operador que no esperabas."),
 (u"Semana 2 · Bucles", u"weeks/2/", u"Repetir sin repetirte, y cuándo conviene cada forma."),
 (u"Semana 3 · Excepciones", u"weeks/3/", u"Que el programa no explote cuando el usuario escribe cualquier cosa."),
 (u"Semana 4 · Bibliotecas", u"weeks/4/", u"Usar lo que ya está escrito, y publicar lo tuyo como paquete."),
 (u"Semana 5 · Pruebas unitarias", u"weeks/5/", u"Probar tu propio código con pytest. Se cruza con la ruta de testing."),
 (u"Semana 6 · Archivos", u"weeks/6/", u"Leer y escribir archivos, CSV incluido, que es la mitad del trabajo con datos."),
 (u"Semana 7 · Expresiones regulares", u"weeks/7/", u"Buscar patrones en texto. Feo de leer y difícil de reemplazar."),
 (u"Semana 8 · Orientación a objetos", u"weeks/8/", u"Clases, atributos y métodos, con la explicación que hace que se entienda."),
 (u"Proyecto final", u"project/", u"Un programa tuyo, en Python, con lo de las nueve semanas."),
]

# --- CS50 SQL: siete semanas, cada una un verbo.
CS50SQL = [
 (u"Semana 0 · Consultar", u"weeks/0/", u"SELECT, filtros y orden. La consulta que vas a escribir todos los días."),
 (u"Semana 1 · Relacionar", u"weeks/1/", u"Varias tablas y cómo se unen: JOINs, claves y por qué existen."),
 (u"Semana 2 · Diseñar", u"weeks/2/", u"Cómo se arma un esquema que no te va a doler en un año."),
 (u"Semana 3 · Escribir", u"weeks/3/", u"INSERT, UPDATE y DELETE, y qué pasa cuando algo falla en el medio."),
 (u"Semana 4 · Ver", u"weeks/4/", u"Vistas: guardar una consulta para no repetirla, y para no mostrar de más."),
 (u"Semana 5 · Optimizar", u"weeks/5/", u"Índices y por qué una consulta que tardaba un minuto tarda un segundo."),
 (u"Semana 6 · Escalar", u"weeks/6/", u"Concurrencia y qué cambia cuando la base la usan muchos a la vez."),
]

# (base, prefijo de id, acto, icono, hue, minutos totales, unidades, nombre)
PARTIR = [
 ("https://cs50.harvard.edu/x/",      "x",  1, "code", "#DC2626", 3600, CS50X,
  u"CS50x"),
 ("https://cs50.harvard.edu/python/", "p",  2, "code", "#EA7A0C", 3000, CS50P,
  u"CS50 Python"),
 ("https://cs50.harvard.edu/sql/",    "q",  2, "sql",  "#2563EB", 2100, CS50SQL,
  u"CS50 SQL"),
]

# Los que quedan enteros: se eligen, no se recorren.
ENTEROS = ["c01", "c05", "c06", "c07", "c08", "c09", "c10", "c11"]


def nodo(nid, act, time, icono, hue, boss, titulo, resumen, meta, wins, url):
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s", hue: "%s"%s,\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "%s"\n'
            u'  }' % (nid, act, time, icono, hue, u", boss: true" if boss else u"",
                      titulo, resumen, meta, w, url))


def main():
    t = io.open(P, encoding="utf-8").read()
    if u"Semana 0 · Scratch" in t:
        print(u"  ya estaba"); sys.exit(1)

    bloque = t[t.index(u"var NODES = ["):]
    bloque = bloque[:bloque.index(u"\n];")]

    # los que se quedan enteros, tal como estan
    viejos = {}
    for m in re.finditer(r'\n  \{\n    id: "(c\d+)".*?\n  \}', bloque, re.S):
        viejos[m.group(1)] = m.group(0).strip()

    salida = []
    for base, pre, acto, icono, hue, minutos, unidades, nombre in PARTIR:
        cada = int(round(minutos / float(len(unidades)) / 5.0)) * 5
        horas = cada // 60
        rato = (u"%d h" % horas) if cada % 60 == 0 else (u"%d h %d min" % (horas, cada % 60))
        for n, (titulo, cola, resumen) in enumerate(unidades):
            salida.append(nodo(
                u"%s%02d" % (pre, n), acto, rato, icono, hue,
                n == 0 and pre == "x",
                u"%s · %s" % (nombre, titulo),
                resumen,
                u"Terminas esta parte cuando entregas su problem set y te compila.",
                [u"Una semana concreta, con su clase y su ejercicio",
                 u"Se marca sola: no hay que terminar el curso entero para avanzar",
                 u"Entra en un bloque de tu semana, que es para lo que existe la agenda"],
                base + cola))

    for cid in ENTEROS:
        if cid not in viejos:
            print(u"  ABORTA: no encuentro el nodo %s" % cid); sys.exit(1)
        salida.append(u"  " + viejos[cid])

    nuevos = u"var NODES = [\n" + u",\n\n".join(salida) + u"\n];"
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nuevos, t, count=1, flags=re.S)

    ACTS = (u'var ACTS = [\n'
            u'  { n: 1, title: "CS50x, semana por semana", desc: "Las once semanas de Harvard y el proyecto final" },\n'
            u'  { n: 2, title: "Python y bases de datos",  desc: "Los otros dos que se hacen enteros, también por semana" },\n'
            u'  { n: 3, title: "Especializarse",           desc: "Cursos completos: se eligen, no se recorren" },\n'
            u'  { n: 4, title: "Para otros roles",         desc: "Tecnología para quien no va a programar" }\n'
            u'];')
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)

    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print(u"cs50.html: %d pasos (%d semanas + %d cursos enteros)"
          % (len(salida), len(salida) - len(ENTEROS), len(ENTEROS)))


main()
