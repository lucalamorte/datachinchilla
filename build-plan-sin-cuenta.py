# -*- coding: utf-8 -*-
u"""El plan se guarda en tu navegador, sin pedirte una cuenta.

   El widget de la agenda se pidio tres veces. Las tres veces lo mire
   con el estado puesto a mano desde la consola, las tres veces
   aparecio, y las tres veces conteste que estaba. Estaba: el widget
   no era el problema.

   El problema es que sin cuenta no llegas a tener plan. El ultimo
   clic del CV -"Guardar mi ruta"- avisaba que hacia falta una cuenta
   y volvia sin guardar nada. Sin rutas activas no hay plan, sin plan
   no hay agenda, y la portada se veia exactamente igual que la de
   alguien que nunca entro. Probandolo deslogueado -que es como se
   prueba el onboarding- el widget no esta nunca.

   Dentro de su propio flujo ese pedido era la excepcion y no la
   regla: el CV, los temas que sacaste o agregaste, las respuestas y
   el puesto ya se venian guardando en localStorage sin cuenta
   ninguna. Se guardaban los cinco pasos y se rechazaba el sexto, que
   es el unico que los vuelve utiles.

   Lo mismo en la semana: sumar o sacar una ruta pedia cuenta, asi que
   ni por ahi se llegaba.

   La cuenta sigue existiendo y sigue sirviendo para lo que decia el
   cartel de la cuenta desde el principio: "Tu avance vive en este
   navegador. Entra con tu mail para llevarlo a otra computadora."
   Eso es sincronizar entre maquinas, no un peaje para usar el sitio.

   No se tocan las rutas: marcar un curso hecho sigue pidiendo cuenta.
   Eso es una decision aparte y no es la que rompe la portada.

   Uso: python build-plan-sin-cuenta.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, viejo, nuevo):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    if nuevo.strip()[:40] in t:
        print(u"  %s: ya estaba" % archivo); return
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: el bloque aparece %d veces, esperaba 1"
              % (archivo, n))
        sys.exit(1)
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(viejo, nuevo, 1))
    print(u"%-14s el guardado ya no pide cuenta" % archivo)


# ------------------------------------------------------------------ el CV
parchar("cv.html", u'''  if(window.PathSync && PathSync.puedeGuardar && !PathSync.puedeGuardar()){
    toast("Para quedarte con tu ruta hace falta una cuenta.");
    try{ openAccount(); }catch(e){ try{ abrirCuenta(); }catch(e2){} }
    return;
  }

''', u'''  /* Sin cuenta tambien se guarda, en este navegador.

     Aca se pedia una, y era la excepcion de su propio flujo: el CV,
     los temas que sacaste o agregaste, las respuestas y el puesto ya
     se guardaban sin cuenta. Se guardaban los cinco pasos y se
     rechazaba el sexto, que es el unico que los vuelve utiles.

     Y el costo no era solo este boton: sin rutas activas no hay
     plan, sin plan no hay agenda, y la portada quedaba igual que la
     de alguien que nunca entro. El widget de la agenda se pidio tres
     veces y estaba puesto las tres: lo que faltaba era el plan.

     La cuenta sigue sirviendo para lo que dice su propio cartel,
     llevarte el avance a otra computadora. Onb.guardar() ya escribe
     en el perfil cuando hay sesion y en localStorage cuando no. */

''')

# -------------------------------------------------------------- la semana
parchar("semana.html", u'''      /* Sacar o sumar una ruta cambia tu semana, o sea tu avance:
         pide cuenta igual que marcar un curso. */
      if(window.PathSync && PathSync.puedeGuardar && !PathSync.puedeGuardar()){
        toast("Para cambiar tu semana hace falta una cuenta.");
        try{ abrirCuenta(); }catch(e){ try{ openAccount(); }catch(e2){} }
        return;
      }
''', u'''      /* Tampoco pide cuenta: es la otra mitad del mismo camino.
         Arreglar el guardado del CV y dejar esto pidiendo cuenta
         seria mover la pared un metro. */
''')
