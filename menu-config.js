/* ═══════════════════════════════════════════════════════════════════════════
   INTERRUPTOR DEL MENÚ DE COMIDA
   ═══════════════════════════════════════════════════════════════════════════

   Hay días con cocina y días sin ella. Cuando no hay comida, la pantalla no
   debe anunciarla: un cliente que ve hamburguesas y se sienta a pedirlas se
   va molesto, y eso cuesta más que la venta que no se hizo.

   PARA APAGARLA:  cambia `true` por `false` en la línea de abajo.
   PARA ENCENDERLA: al revés.

   Guarda el cambio y ya. La pantalla se recarga sola cada 5 minutos, así que
   el televisor se entera sin que nadie lo toque. No hace falta reiniciar nada
   ni entrar al local.

   Si se edita desde el teléfono por GitHub, es la única palabra que hay que
   cambiar en todo el archivo.
   ═══════════════════════════════════════════════════════════════════════════ */

window.HAY_COMIDA = true;

/* ───────────────────────────────────────────────────────────────────────────
   Cuántos segundos se queda cada lámina antes de pasar a la siguiente.

   Doce es lo que tarda alguien de pie en una barra en leer una columna de
   precios. Menos, y se pierde a mitad; más, y quien llegó buscando comida
   cree que solo hay cerveza.
   ─────────────────────────────────────────────────────────────────────────── */

window.SEGUNDOS_POR_LAMINA = 12;
