/* ═══════════════════════════════════════════════════════════════════════════
   INTERRUPTOR DEL MENÚ DE COMIDA
   ═══════════════════════════════════════════════════════════════════════════

   Hay días con cocina y días sin ella. Cuando no hay comida, la pantalla no
   debe anunciarla: un cliente que ve hamburguesas y se sienta a pedirlas se
   va molesto, y eso cuesta más que la venta que no se hizo.

   QUÉ SE ESCRIBE EN LA LÍNEA DE ABAJO — una de estas tres, con comillas:

       'chilea'   → se anuncia el menú de Chilea Burger Lab
       'chona'    → se anuncia el menú de La Chona
       false      → no hay comida: solo cervezas   (SIN comillas)

   Cualquier otra cosa —una errata, un popup que no existe— apaga la comida.
   Eso es a propósito: entre anunciar el menú equivocado y no anunciar nada,
   no anunciar nada es lo barato. Un cliente que ve hamburguesas que hoy no
   se venden se va molesto; uno que no las ve, pregunta.

   Para añadir un popup nuevo hace falta además su lámina en el HTML, con el
   id `lamina-<nombre>`. Sin eso, escribir su nombre aquí apaga la comida.

   Guarda el cambio y ya. El televisor le pregunta a este archivo cada 45
   segundos saltándose los dos cachés que hay en medio —el suyo y el de
   GitHub— y se recarga solo en cuanto ve que cambió. Cuenta con menos de un
   minuto desde que guardas, más lo que GitHub tarde en publicar el commit,
   que suele ser medio minuto. No hace falta reiniciar nada, ni entrar al
   local, ni hacer Ctrl+Shift+R nunca más.

   Si pasados dos minutos la pantalla sigue igual, el problema ya no es el
   caché: mira en la pestaña Actions del repositorio si el commit se publicó.

   Si se edita desde el teléfono por GitHub, es la única palabra que hay que
   cambiar en todo el archivo.
   ═══════════════════════════════════════════════════════════════════════════ */

window.HAY_COMIDA = 'chilea';

/* ───────────────────────────────────────────────────────────────────────────
   Cuántos segundos se queda cada lámina antes de pasar a la siguiente.

   Doce es lo que tarda alguien de pie en una barra en leer una columna de
   precios. Menos, y se pierde a mitad; más, y quien llegó buscando comida
   cree que solo hay cerveza.
   ─────────────────────────────────────────────────────────────────────────── */

window.SEGUNDOS_POR_LAMINA = 20;
