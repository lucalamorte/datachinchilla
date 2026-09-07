# -*- coding: utf-8 -*-
u"""Que "no se Docker" deje de contar como saber Docker.

   El motor busca cada senal de tema como palabra suelta y, si la
   encuentra, da el tema por sabido. No mira lo que hay alrededor. O
   sea que "no tengo experiencia en Spark" y "cinco anos con Spark"
   valen exactamente lo mismo, y a alguien que aclara lo que le falta
   se le ofrece la ruta de alguien que ya lo sabe.

   No es un caso raro. Es lo que hace todo el mundo cuando le
   preguntan que sabe: contesta tambien que no sabe. Y la caja de
   texto del onboarding invita a eso mas todavia que un CV.

   Como se resuelve: cada aparicion de la senal se mira con lo que
   tiene delante, hasta el corte de frase mas cercano. Si ahi hay una
   negacion, esa aparicion no cuenta. La senal se cae solo si TODAS
   sus apariciones estan negadas: "no se Docker avanzado, pero uso
   Docker a diario" tiene que seguir contando.

   Tres cuidados, que son los que hacen que esto no rompa mas de lo
   que arregla:

   1. La frase corta. "No termine la carrera. Python desde 2019" no
      es una negacion de Python: el punto los separa. Se corta en
      punto, punto y coma, salto de linea, vineta y guion de lista.
   2. "no solo Python sino tambien R" no niega Python. "no" seguido
      de solo, solamente, unicamente u obstante no es una negacion.
   3. "sin" solo cuenta pegado a la senal o en frase hecha -sin
      experiencia, sin conocimientos, sin manejo-, porque "sin
      problemas con Docker" es lo contrario de una negacion.

   Lo que se cuenta como no saber, ademas de la negacion: querer
   aprenderlo. "Ganas de aprender Kubernetes" no es saber Kubernetes,
   y aparece en la mitad de los CV junior.

   Uso: python build-negaciones.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cv.js")

VIEJO = u'''  /* Una señal cuenta sólo si aparece como palabra suelta o frase, no
     dentro de otra. Sin esto "r" o "java" pescarían medio CV. */
  function apareceEn(texto, senal){
    var esc = senal.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
    return new RegExp("(^|[^a-z0-9])" + esc + "([^a-z0-9]|$)").test(texto);
  }'''

NUEVO = u'''  /* ---------------------------------------------------------------
     LO QUE NO SE SABE

     El motor buscaba la señal y, si estaba, daba el tema por sabido.
     No miraba lo que tenía alrededor: "no tengo experiencia en Spark"
     y "cinco años con Spark" valían igual, así que a quien aclaraba
     lo que le falta se le ofrecía la ruta de quien ya lo sabe.

     No es un caso raro: es lo que hace todo el mundo cuando le
     preguntan qué sabe. Contesta también qué no sabe.
     --------------------------------------------------------------- */

  /* Hasta acá se mira hacia atrás. Una negación que quede más lejos
     que esto ya está hablando de otra cosa. */
  var VENTANA = 46;

  /* Corta la frase. "No terminé la carrera. Python desde 2019" no
     niega Python: el punto los separa. */
  var CORTE = /[.;:\\n\\r\\u2022\\u00b7|]|(^|\\s)[-*]\\s/;

  var NIEGAN = [
    "no se", "no tengo", "no cuento con", "no manejo", "no domino",
    "no conozco", "no use", "no usé", "no he usado", "no he trabajado",
    "no trabaje", "no llegue a", "no alcance a", "no toque",
    "nunca use", "nunca usé", "nunca he", "nunca trabaje", "nunca toque",
    "desconozco", "cero", "nada de", "poco y nada de",
    "sin experiencia", "sin conocimiento", "sin conocimientos",
    "sin manejo", "sin saber", "sin haber", "sin practica",
    /* Querer aprenderlo no es saberlo, y está en medio CV junior. */
    "ganas de aprender", "quiero aprender", "quisiera aprender",
    "me gustaria aprender", "me interesa aprender", "interes en aprender",
    "aprendiendo a", "por aprender", "pendiente de aprender",
    "me falta", "me faltan", "asignatura pendiente"
  ];

  /* "no solo Python sino también R" no niega Python. */
  var NO_NIEGA = ["solo", "solamente", "unicamente", "obstante", "pocas"];

  function niega(previo){
    /* Sólo desde el último corte: más atrás es otra frase. */
    var m = previo.split(CORTE);
    var frase = m[m.length - 1];
    var i, j, pos, resto;

    for(i=0;i<NIEGAN.length;i++){
      pos = frase.lastIndexOf(NIEGAN[i]);
      if(pos < 0) continue;
      if(NIEGAN[i].indexOf("no ") === 0){
        resto = frase.slice(pos + 3).replace(/^\\s+/, "");
        for(j=0;j<NO_NIEGA.length;j++){
          if(resto.indexOf(NO_NIEGA[j]) === 0) { pos = -1; break; }
        }
        if(pos < 0) continue;
      }
      return true;
    }
    /* "sin Docker" pegado. Suelto no: "sin problemas con Docker" es
       lo contrario de una negación. */
    return /(^|[^a-z])sin\\s+[a-z0-9 ]{0,12}$/.test(frase);
  }

  /* Una señal cuenta sólo si aparece como palabra suelta o frase, no
     dentro de otra. Sin esto "r" o "java" pescarían medio CV.

     Y cuenta sólo si alguna de sus apariciones no está negada: se
     cae entera únicamente cuando TODAS lo están, porque "no sé
     Docker avanzado, pero uso Docker a diario" tiene que seguir
     contando. */
  function apareceEn(texto, senal){
    var esc = senal.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
    var re = new RegExp("(^|[^a-z0-9])" + esc + "([^a-z0-9]|$)", "g");
    var m, hubo = false;
    while((m = re.exec(texto)) !== null){
      hubo = true;
      var ini = m.index + m[1].length;
      if(!niega(texto.slice(Math.max(0, ini - VENTANA), ini))) return true;
      if(re.lastIndex <= m.index) re.lastIndex = m.index + 1;
    }
    return hubo ? false : false;
  }'''

t = io.open(P, encoding="utf-8").read()
if "NIEGAN" in t:
    print(u"  ya estaba"); sys.exit(1)
if t.count(VIEJO) != 1:
    print(u"  ABORTA: apareceEn aparece %d veces" % t.count(VIEJO)); sys.exit(1)
io.open(P, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
print(u"cv.js: lo que el CV dice que no sabe deja de contar")
