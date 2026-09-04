# -*- coding: utf-8 -*-
"""Chequeo de tuteo. Se corre antes de dar cualquier cosa por lista.

   La regla del proyecto es tuteo siempre, sin excepciones, y el voseo
   se cuela cada vez que se escribe texto nuevo, porque es como se
   habla. Un chequeo que hay que acordarse de correr no sirve; este
   esta pensado para correrlo despues de cada cambio de copy, junto
   con build-brand.py.

   Mira el archivo entero, no solo el HTML visible: buena parte del
   texto lo arma el JavaScript.

   Con --arreglar aplica los reemplazos que sabe hacer y lista los que
   necesitan ojo humano.
"""
import io, re, sys, glob, os, unicodedata

D = u"C:/Users/Luca/Desktop/snowflake path/"

# Voseo -> tuteo. Los verbos que diptongan van completos, porque no
# alcanza con sacarle el acento a la ultima silaba: "tenes" no es
# "tenes" sino "tienes".
PARES = [
 # imperativos
 (u"Pegá", u"Pega"), (u"pegá", u"pega"),
 (u"Contá", u"Cuenta"), (u"contá", u"cuenta"),
 (u"Soltá", u"Suelta"), (u"soltá", u"suelta"),
 (u"Pasá", u"Pasa"), (u"pasá", u"pasa"),
 (u"Probá", u"Prueba"), (u"probá", u"prueba"),
 (u"Entrá", u"Entra"), (u"entrá", u"entra"),
 (u"Poné", u"Pon"), (u"poné", u"pon"),
 (u"Mirá", u"Mira"), (u"mirá", u"mira"),
 (u"Andá", u"Anda"), (u"andá", u"anda"),
 (u"Hacé", u"Haz"), (u"hacé", u"haz"),
 (u"Vení", u"Ven"), (u"vení", u"ven"),
 (u"Tené", u"Ten"), (u"tené", u"ten"),
 (u"Dejá", u"Deja"), (u"dejá", u"deja"),
 (u"Sumá", u"Suma"), (u"sumá", u"suma"),
 (u"Anotá", u"Anota"), (u"anotá", u"anota"),
 (u"Guardá", u"Guarda"), (u"guardá", u"guarda"),
 (u"Empezá", u"Empieza"), (u"empezá", u"empieza"),
 (u"Buscá", u"Busca"), (u"buscá", u"busca"),
 (u"Armá", u"Arma"), (u"armá", u"arma"),
 (u"Marcá", u"Marca"), (u"marcá", u"marca"),
 (u"Borrá", u"Borra"), (u"borrá", u"borra"),
 (u"Cambialo", u"Cámbialo"), (u"cambialo", u"cámbialo"),
 (u"Fijate", u"Fíjate"), (u"fijate", u"fíjate"),
 (u"Decime", u"Dime"), (u"decime", u"dime"),
 (u"Decinos", u"Dinos"), (u"decinos", u"dinos"),
 (u"Acordate", u"Acuérdate"), (u"acordate", u"acuérdate"),
 (u"Sacá", u"Saca"), (u"sacá", u"saca"),
 (u"preferís", u"prefieres"), (u"Preferís", u"Prefieres"),
 (u"venís", u"vienes"), (u"Venís", u"Vienes"),
 (u"salís", u"sales"), (u"seguís", u"sigues"), (u"Seguís", u"Sigues"),
 (u"vivís", u"vives"), (u"decís", u"dices"), (u"Decís", u"Dices"),
 (u"hacés", u"haces"), (u"Hacés", u"Haces"),
 (u"ponés", u"pones"), (u"Ponés", u"Pones"),
 (u"volvés", u"vuelves"), (u"conocés", u"conoces"),
 (u"elegís", u"eliges"), (u"Elegís", u"Eliges"),
 (u"pedís", u"pides"), (u"medís", u"mides"),
 (u"Mandá", u"Manda"), (u"mandá", u"manda"),
 (u"Contalo", u"Cuéntalo"), (u"contalo", u"cuéntalo"),
 (u"Llevá", u"Lleva"), (u"llevá", u"lleva"),
 (u"Tomá", u"Toma"), (u"tomá", u"toma"),
 (u"Usá", u"Usa"), (u"usá", u"usa"),
 (u"Cerrá", u"Cierra"), (u"cerrá", u"cierra"),
 (u"Agregá", u"Agrega"), (u"agregá", u"agrega"),
 (u"Apretá", u"Aprieta"), (u"apretá", u"aprieta"),
 (u"Tocá", u"Toca"), (u"tocá", u"toca"),
 (u"Retomá", u"Retoma"), (u"retomá", u"retoma"),
 (u"Armala", u"Ármala"), (u"armala", u"ármala"),
 (u"Cambiá", u"Cambia"), (u"cambiá", u"cambia"),
 (u"ordenás", u"ordenas"), (u"dedicás", u"dedicas"),
 (u"Elegís", u"Eliges"), (u"llevás", u"llevas"),
 (u"Mostrame", u"Muéstrame"), (u"mostrame", u"muéstrame"),
 (u"arrancás", u"arrancas"), (u"Arrancás", u"Arrancas"),
 (u"Mostrá", u"Muestra"), (u"mostrá", u"muestra"),
 (u"Contame", u"Cuéntame"), (u"contame", u"cuéntame"),
 (u"Compará", u"Compara"), (u"compará", u"compara"),
 (u"Revisá", u"Revisa"), (u"revisá", u"revisa"),
 (u"Practicá", u"Practica"), (u"practicá", u"practica"),
 (u"Repasá", u"Repasa"), (u"repasá", u"repasa"),
 # imperativo con pronombre pegado: el voseo no lleva tilde
 (u"sacala", u"sácala"), (u"Sacala", u"Sácala"),
 (u"sacalo", u"sácalo"), (u"Sacalo", u"Sácalo"),
 (u"cambiala", u"cámbiala"), (u"Cambiala", u"Cámbiala"),
 (u"dejalo", u"déjalo"), (u"Dejalo", u"Déjalo"),
 (u"dejala", u"déjala"), (u"Dejala", u"Déjala"),
 (u"miralo", u"míralo"), (u"Miralo", u"Míralo"),
 (u"probalo", u"pruébalo"), (u"Probalo", u"Pruébalo"),
 (u"anotalo", u"anótalo"), (u"Anotalo", u"Anótalo"),
 (u"guardalo", u"guárdalo"), (u"Guardalo", u"Guárdalo"),
 (u"marcalo", u"márcalo"), (u"Marcalo", u"Márcalo"),
 (u"tocalo", u"tócalo"), (u"Tocalo", u"Tócalo"),
 (u"buscalo", u"búscalo"), (u"Buscalo", u"Búscalo"),
 (u"usalo", u"úsalo"), (u"Usalo", u"Úsalo"),
 (u"borralo", u"bórralo"), (u"Borralo", u"Bórralo"),
 (u"borrala", u"bórrala"), (u"Borrala", u"Bórrala"),
 (u"contame", u"cuéntame"), (u"Contame", u"Cuéntame"),
 (u"avisame", u"avísame"), (u"Avisame", u"Avísame"),
 (u"fijate", u"fíjate"),
 # presentes
 (u"tenés", u"tienes"), (u"Tenés", u"Tienes"),
 (u"podés", u"puedes"), (u"Podés", u"Puedes"),
 (u"querés", u"quieres"), (u"Querés", u"Quieres"),
 (u"sabés", u"sabes"), (u"Sabés", u"Sabes"),
 (u"apuntás", u"apuntas"), (u"Apuntás", u"Apuntas"),
 (u"entendés", u"entiendes"), (u"Entendés", u"Entiendes"),
 (u"aprendés", u"aprendes"), (u"practicás", u"practicas"),
 (u"armás", u"armas"), (u"terminás", u"terminas"),
 (u"estudiás", u"estudias"), (u"Estudiás", u"Estudias"),
 (u"parás", u"paras"), (u"leés", u"lees"),
 (u"defendés", u"defiendes"), (u"desplegás", u"despliegas"),
 (u"entregás", u"entregas"), (u"convertís", u"conviertes"),
 (u"reemplazás", u"reemplazas"), (u"explicás", u"explicas"),
 (u"arreglás", u"arreglas"), (u"destruís", u"destruyes"),
 (u"levantás", u"levantas"), (u"necesitás", u"necesitas"),
 (u"llevás", u"llevas"), (u"dejás", u"dejas"),
 (u"buscás", u"buscas"), (u"marcás", u"marcas"),
 (u"vas a tener", u"vas a tener"),
]

# Verbos en -ir: el imperativo voseante y la primera persona del
# preterito se escriben igual ("escribi" es "escribi vos" y tambien "yo
# escribi"). No se arreglan solos: se muestran con su frase para que
# decida una persona.
AMBIGUOS = [u"escribí", u"elegí", u"seguí", u"abrí", u"subí", u"viví",
            u"salí", u"recibí", u"definí", u"decidí", u"repetí",
            u"conseguí", u"perdí", u"medí", u"permití", u"insistí"]

# Primera persona del pasado: iguales en tuteo y voseo, no se tocan.
# Se listan para que el barrido general no las reporte cada vez.
LEGITIMAS = set(u"""
está acá allá aquí ahí así también según además día días sí ningún
algún común jamás quizá café aún más solo país através través estás
estés escribí armé puse hice vi fui leí seguí conseguí subí abrí
perdí elegí definí decidí repetí recibí guardé terminé completé tomé
creé entré encontré aprendí nací salí viví qué cuál cuáles quién
quiénes cómo cuándo dónde adónde porqué caché
""".split())

def ARCHIVOS():
    """Las paginas, los modulos y los generadores. Los .py entran
       porque ahi es donde se escribe el copy antes de bajar al HTML;
       arreglar solo el HTML dura hasta la proxima corrida."""
    return (sorted(glob.glob(D + u"*.html")) +
            sorted(glob.glob(D + u"*.js")) +
            sorted(glob.glob(D + u"build-*.py")))


PAL = re.compile(u"[A-Za-zÁÉÍÓÚÑáéíóúñ]{3,}[áéí](?![A-Za-zÁÉÍÓÚÑáéíóúñ])")


def revisar(arreglar=False):
    tocados, restos = [], []
    for p in ARCHIVOS():
        t = io.open(p, encoding="utf-8").read()
        t0, n = t, 0
        for a, b in PARES:
            if a == b:
                continue
            c = len(re.findall(u"(?<![A-Za-zÁÉÍÓÚÑáéíóúñ])" + re.escape(a) +
                               u"(?![A-Za-zÁÉÍÓÚÑáéíóúñ])", t))
            if c:
                if arreglar:
                    t = re.sub(u"(?<![A-Za-zÁÉÍÓÚÑáéíóúñ])" + re.escape(a) +
                               u"(?![A-Za-zÁÉÍÓÚÑáéíóúñ])", b, t)
                n += c
        if n:
            tocados.append((os.path.basename(p), n))
            if arreglar and t != t0:
                io.open(p, "w", encoding="utf-8", newline="").write(t)

        # lo que el diccionario no cubre, para mirar a ojo
        limpio = re.sub(u"<!--.*?-->", u" ", t, flags=re.S)
        limpio = re.sub(u"/\\*.*?\\*/", u" ", limpio, flags=re.S)
        for m in PAL.finditer(limpio):
            w = m.group(0)
            if w.lower() in LEGITIMAS:
                continue
            restos.append((os.path.basename(p), w))
    return tocados, restos


arreglar = "--arreglar" in sys.argv
tocados, restos = revisar(arreglar)

if tocados:
    verbo = u"corregidas" if arreglar else u"encontradas"
    print(u"Formas de voseo %s:" % verbo)
    for a, n in tocados:
        print(u"  %-22s %d" % (a, n))
else:
    print(u"Sin voseo conocido.")

ambiguos = []
for _p in ARCHIVOS():
    _t = io.open(_p, encoding="utf-8").read()
    for _v in AMBIGUOS:
        for _m in re.finditer(u"(?<![A-Za-zÁÉÍÓÚÑáéíóúñ])" + _v +
                              u"(?![A-Za-zÁÉÍÓÚÑáéíóúñ])", _t, re.I):
            ambiguos.append((os.path.basename(_p),
                             _t[max(0, _m.start()-55):_m.end()+35].replace(u"\n", u" ")))
if ambiguos:
    print(u"\nAmbiguos, decide una persona (imperativo o pasado):")
    for _a, _f in ambiguos[:12]:
        print(u"  %-18s ...%s..." % (_a, _f.strip()))

if restos:
    vistos = sorted(set(restos))
    print(u"\nA revisar a ojo (%d):" % len(vistos))
    for a, w in vistos[:25]:
        print(u"  %-22s %s" % (a, w))

if tocados and not arreglar:
    print(u"\n  Corre: python tuteo.py --arreglar")
    sys.exit(1)
