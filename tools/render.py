#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenera la lamina de BEBIDAS de cervezas-camacho.html desde menu-data.json.

Fuente de verdad de las bebidas = menu-data.json. Este script es lo UNICO que
toca el HTML de bebidas; asi el modelo/la gente no edita HTML a mano.

Uso:  python3 tools/render.py            # renderiza al repo (ruta por defecto)
      python3 tools/render.py <html> <json>
Anclas: desde '<div class="slide on">' hasta '</div><!-- /slide bebidas -->'.
Idempotente: dos corridas seguidas dan el mismo archivo.
"""
import sys, os, html, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (tools/ esta un nivel debajo)

def esc(t):
    return html.escape(str(t), quote=False)

def item_html(it):
    cls = "item compact" if it.get("compact") else "item"
    desc = it.get("desc", "")
    desc_line = ('\n          <div class="item-desc">%s</div>' % esc(desc)) if desc != "" else ''
    return ('      <div class="%s">\n'
            '        <div class="item-info">\n'
            '          <div class="item-name">%s</div>%s\n'
            '        </div>\n'
            '        <span class="item-price">%s</span>\n'
            '      </div>\n') % (cls, esc(it["nombre"]), desc_line, esc(it.get("precio", "")))

def generar(data):
    izq = [s for s in data["secciones"] if s.get("columna") == "izquierda"]
    dere = [s for s in data["secciones"] if s.get("columna") != "izquierda"]
    if not izq:
        raise SystemExit("menu-data.json: hace falta una seccion de columna 'izquierda' (Del Grifo)")

    left = ('      <div class="sec-title">%s</div>\n'
            '      <div class="sec-rule"></div>\n\n' % esc(izq[0]["titulo"]))
    left += "".join(item_html(it) for it in izq[0]["items"])

    right = ""
    for i, sec in enumerate(dere):
        if i:
            right += "\n"
        gap = " sec-gap" if sec.get("gap") else ""
        right += ('      <div class="sec-title%s">%s</div>\n'
                  '      <div class="sec-rule"></div>\n\n' % (gap, esc(sec["titulo"])))
        right += "".join(item_html(it) for it in sec["items"])

    upsell = "".join('        <div class="upsell-label">%s</div>\n'
                     '        <div class="upsell-value">%s</div>\n' % (esc(u["label"]), esc(u["value"]))
                     for u in data.get("upsell", []))

    return ('<div class="slide on">\n'
            '  <div class="grid">\n\n'
            '    <!-- LEFT: DEL GRIFO -->\n'
            '    <div class="col">\n'
            '     <div class="col-inner">\n'
            + left +
            '     </div><!-- /col-inner -->\n'
            '    </div>\n\n'
            '    <!-- CENTER: LOGO -->\n'
            '    <div class="center">\n'
            '      <img class="logo-img" src="media/logo-griferia-ajustado.png" alt="La Grifería">\n'
            '      <div class="upsell">\n' + upsell +
            '      </div>\n'
            '      <div class="site">www.lagriferiapr.com</div>\n'
            '    </div>\n\n'
            '    <!-- RIGHT: TRAGOS + LATAS -->\n'
            '    <div class="col">\n'
            '     <div class="col-inner">\n'
            + right +
            '     </div><!-- /col-inner -->\n'
            '    </div>\n\n'
            '  </div>\n'
            '  </div><!-- /slide bebidas -->')

def escribir(cervezas, jsonpath):
    data = json.load(open(jsonpath, encoding="utf-8"))
    s = open(cervezas, encoding="utf-8").read()
    ini = s.find('<div class="slide on">')
    fin_marker = '</div><!-- /slide bebidas -->'
    fin = s.find(fin_marker)
    if ini == -1 or fin == -1:
        raise SystemExit("NO ENCONTRE las anclas de la lamina de bebidas. No toco el archivo. "
                         "Alguien movio <div class=\"slide on\"> o '</div><!-- /slide bebidas -->'.")
    if s.count('<div class="slide on">') != 1 or s.count(fin_marker) != 1:
        raise SystemExit("Las anclas de la lamina de bebidas no son unicas. Aborto para no romper nada.")
    nuevo = s[:ini] + generar(data) + s[fin + len(fin_marker):]
    open(cervezas, "w", encoding="utf-8").write(nuevo)
    return nuevo != s

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "cervezas-camacho.html")
    j = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "menu-data.json")
    changed = escribir(c, j)
    print("rendered:", c, "(cambio)" if changed else "(ya estaba al dia)")
