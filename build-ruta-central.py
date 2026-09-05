# -*- coding: utf-8 -*-
"""Una ruta que no toca el oficio no es tu ruta.

   Con un CV de desarrollador React apuntando a Full Stack, el sitio
   recomendaba SnowPro Core. No es un error de vocabulario: los temas
   se reconocian bien -desarrollo web, backend, fundamentos-. Es la
   regla de puntuacion.

   Se elegia por cuanto de lo que te falta cubre la ruta, y todos los
   temas pesaban por igual en esa cuenta. SnowPro tiene dieciseis
   pasos de nube y SQL, que un full stack tambien necesita un poco,
   asi que sumaba mas que las quince partes de Full Stack Open, que
   cubren justo lo que el puesto es.

   La regla que faltaba: el puesto pide algunos temas en 3, y esos son
   el oficio. Una ruta que no toca ninguno de los que te faltan puede
   ser util despues, pero no es la que se recomienda como TU ruta.

   Se filtra en vez de ponderar porque es una regla que se puede
   explicar en una linea, y porque ponderar deja pasar el caso raro
   igual, solo que mas dificil de ver.

   Uso: python build-ruta-central.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "onboarding.js")

VIEJO = u'''    var rs = (typeof PASOS !== "undefined") ? PASOS : [], out = [], j, k;
    var nivel = miNivel();
    for(j=0;j<rs.length;j++){
      var clave = rs[j].clave;
      if(clave === "de") continue;          /* es un mapa, no una ruta */
      /* Una ruta que arranca más arriba de donde estás no es tu
         ruta, por mucho que cubra los temas que te faltan. */
      if((rs[j].nivelN || 0) > nivel) continue;
      var temas = temasDeRuta(clave);
      var cubre = 0, pasosUtiles = 0, pasosTotal = 0;
      for(k in temas){
        pasosTotal += temas[k];
        if(falta[k]){ cubre += falta[k]; pasosUtiles += temas[k]; }
      }
      if(!pasosTotal) continue;
      out.push({
        clave: clave,
        nombre: rs[j].nombre,
        archivo: rs[j].archivo,
        /* Cuánto de lo que te falta resuelve esta ruta. */
        cubre: cubre / pesoTotal,
        /* Cuánto de la ruta te sirve: si la mitad ya la sabes, no
           es tu ruta aunque cubra los temas. */
        aprovecha: pasosUtiles / pasosTotal,
        pasos: rs[j].pasos.length
      });
    }
    out.sort(function(a, b){
      return (b.cubre * b.aprovecha) - (a.cubre * a.aprovecha);
    });
    return out;
  }'''

NUEVO = u'''    /* Los temas que son el oficio: los que el puesto pide en 3 y
       todavía te faltan. Una ruta que no toca ninguno puede servirte
       después, pero no es TU ruta.

       Sin esta regla, a un desarrollador de React apuntando a Full
       Stack le salía SnowPro Core: dieciséis pasos de nube y SQL, que
       también le hacen falta un poco, sumaban más que las quince
       partes que cubren justo lo que el puesto es. Todos los temas
       pesaban igual en la cuenta. */
    var puesto = (typeof CV !== "undefined") ? CV.puestoDe(estado.puesto) : null;
    var pide = (puesto && puesto.temas) ? puesto.temas : {};
    var centrales = [], kk;
    for(kk in falta){ if(pide[kk] >= 3) centrales.push(kk); }

    var rs = (typeof PASOS !== "undefined") ? PASOS : [], out = [], j, k;
    var nivel = miNivel();
    for(j=0;j<rs.length;j++){
      var clave = rs[j].clave;
      if(clave === "de") continue;          /* es un mapa, no una ruta */
      /* Una ruta que arranca más arriba de donde estás no es tu
         ruta, por mucho que cubra los temas que te faltan. */
      if((rs[j].nivelN || 0) > nivel) continue;
      var temas = temasDeRuta(clave);
      var cubre = 0, pasosUtiles = 0, pasosTotal = 0;
      for(k in temas){
        pasosTotal += temas[k];
        if(falta[k]){ cubre += falta[k]; pasosUtiles += temas[k]; }
      }
      if(!pasosTotal) continue;

      var tocaCentral = 0, c;
      for(c=0;c<centrales.length;c++){ if(temas[centrales[c]]) tocaCentral++; }
      /* Si el puesto tiene oficio declarado y esta ruta no toca nada
         de él, queda afuera de la recomendación. */
      if(centrales.length && !tocaCentral) continue;

      out.push({
        clave: clave,
        nombre: rs[j].nombre,
        archivo: rs[j].archivo,
        /* Cuánto de lo que te falta resuelve esta ruta. */
        cubre: cubre / pesoTotal,
        /* Cuánto de la ruta te sirve: si la mitad ya la sabes, no
           es tu ruta aunque cubra los temas. */
        aprovecha: pasosUtiles / pasosTotal,
        /* Cuántos de los temas centrales del puesto toca. Desempata:
           entre dos rutas parecidas, la que va más al centro. */
        central: centrales.length ? tocaCentral / centrales.length : 0,
        pasos: rs[j].pasos.length
      });
    }
    out.sort(function(a, b){
      var pa = a.cubre * a.aprovecha * (1 + a.central);
      var pb = b.cubre * b.aprovecha * (1 + b.central);
      return pb - pa;
    });
    return out;
  }'''

t = io.open(P, encoding="utf-8").read()
if t.count(VIEJO) != 1:
    print(u"  ABORTA: el ancla aparece %d veces, esperaba 1" % t.count(VIEJO))
    sys.exit(1)
io.open(P, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
print(u"onboarding.js: la ruta recomendada tiene que tocar el oficio")
