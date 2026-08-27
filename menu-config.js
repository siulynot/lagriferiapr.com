/* ═══════════════════════════════════════════════════════════════════════════
   INTERRUPTOR DEL MENÚ DE COMIDA
   ═══════════════════════════════════════════════════════════════════════════

   Hay días con cocina y días sin ella. Cuando no hay comida, la pantalla no
   debe anunciarla: un cliente que ve hamburguesas y se sienta a pedirlas se
   va molesto, y eso cuesta más que la venta que no se hizo.

   PARA APAGARLA:  cambia `true` por `false` en la línea de abajo.
   PARA ENCENDERLA: al revés.

   Guarda el cambio y ya. La pantalla se recarga sola cada 5 minutos y pide
   este archivo sin pasar por su caché, así que el televisor se entera solo en
   ese plazo. No hace falta reiniciar nada ni entrar al local.

   Si necesitas que sea AHORA MISMO, recarga la página en el televisor
   (Ctrl+Shift+R o Cmd+Shift+R).

   Si se edita desde el teléfono por GitHub, es la única palabra que hay que
   cambiar en todo el archivo.
   ═══════════════════════════════════════════════════════════════════════════ */

window.HAY_COMIDA = false;

/* ───────────────────────────────────────────────────────────────────────────
   Cuántos segundos se queda cada lámina antes de pasar a la siguiente.

   Doce es lo que tarda alguien de pie en una barra en leer una columna de
   precios. Menos, y se pierde a mitad; más, y quien llegó buscando comida
   cree que solo hay cerveza.
   ─────────────────────────────────────────────────────────────────────────── */

window.SEGUNDOS_POR_LAMINA = 20;
