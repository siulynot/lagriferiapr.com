#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Edita las bebidas del menu (menu-data.json) y regenera el HTML.

Disenado para que un modelo/agente lo llame sin pensar mucho: hace la edicion
de forma deterministica y se NEGUEGA si falta un dato o si el nombre no es
unico, en vez de adivinar. Nunca inventa precios.

Comandos:
  list
  add     --seccion "Del Grifo" --nombre X [--desc Y] --precio "$8" [--compact] [--after N | --posicion K]
  edit    --seccion "Del Grifo" --nombre X [--nuevonombre Z] [--desc Y] [--precio "$9"] [--compacto si|no]
  remove  --seccion "Del Grifo" --nombre X
  price   --seccion "Del Grifo" --nombre X --precio "$8"
  --dry-run : muestra el cambio y el diff de HTML, NO escribe.
Salida: siempre termina con 'dry-run' o el diff 'git diff' de lo que cambio.
"""
import sys, os, re, json, argparse, difflib, subprocess, copy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON = os.path.join(ROOT, "menu-data.json")
HTML = os.path.join(ROOT, "cervezas-camacho.html")
sys.path.insert(0, HERE)
import render

def carga():
    return json.load(open(JSON, encoding="utf-8"))

def seccion(data, nombre):
    for s in data["secciones"]:
        if s["titulo"].lower() == nombre.lower():
            return s
    raise SystemExit("ERROR seccion: '%s' no existe. Validas: %s" % (nombre, ", ".join(s["titulo"] for s in data["secciones"])))

def busca_item(sec, nombre):
    hits = [i for i, it in enumerate(sec["items"]) if it["nombre"].lower() == nombre.lower()]
    if len(hits) == 1:
        return hits[0]
    if len(hits) == 0:
        cerca = difflib.get_close_matches(nombre, [it["nombre"] for it in sec["items"]], n=3, cutoff=0.5)
        raise SystemExit("ERROR item: '%s' no esta en '%s'. Quisiste decir: %s" % (nombre, sec["titulo"], cerca or "ninguno"))
    raise SystemExit("ERROR item: '%s' aparece %d veces en '%s'. Renombra una antes de editar." % (nombre, len(hits), sec["titulo"]))

def normaliza_precio(p):
    p = p.strip()
    if not re.fullmatch(r"\$?\d+(\.\d+)?", p):
        raise SystemExit("ERROR precio: '%s' no es un precio. Formato: $8 o 8 o 8.50 (no lo invento)." % p)
    return "$" + p.lstrip("$")

def guardar(data):
    open(JSON, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

def diff_json(a, b):
    ja = json.dumps(a, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    jb = json.dumps(b, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    return "\n".join(difflib.unified_diff(ja, jb, "menu-data.json (antes)", "menu-data.json (despues)", lineterm=""))

def git_diff_html():
    try:
        return subprocess.run(["git", "-C", ROOT, "diff", "--", "cervezas-camacho.html"],
                              capture_output=True, text=True).stdout
    except Exception:
        return "(git diff no disponible)"

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    apn = lambda name: [sub.add_parser(name)]
    for name in ["list", "add", "edit", "remove", "price"]:
        p = sub.add_parser(name)
        p.add_argument("--seccion", default="Del Grifo")
        p.add_argument("--nombre")
        p.add_argument("--nuevonombre")
        p.add_argument("--desc")
        p.add_argument("--precio")
        p.add_argument("--after")
        p.add_argument("--posicion", type=int)
        p.add_argument("--compact", action="store_true")
        p.add_argument("--compacto", choices=["si", "no"])
        p.add_argument("--dry-run", action="store_true")

    a = ap.parse_args()
    data = carga()
    antes = copy.deepcopy(data)

    if a.cmd == "list":
        for s in data["secciones"]:
            print("[%s]" % s["titulo"])
            for it in s["items"]:
                print("   - %s | %s | %s%s" % (it["nombre"], it.get("desc", ""), it.get("precio", ""),
                                               "  (compact)" if it.get("compact") else ""))
        return

    if a.cmd == "add":
        if not a.nombre:
            raise SystemExit("ERROR add: falta --nombre.")
        if not a.precio:
            raise SystemExit("ERROR add: falta --precio. NO lo invento: preguntale a Luis cuanto cuesta.")
        sec = seccion(data, a.seccion)
        if any(it["nombre"].lower() == a.nombre.lower() for it in sec["items"]):
            raise SystemExit("ERROR add: '%s' ya existe en '%s'. Usa edit, o cambiale el nombre." % (a.nombre, sec["titulo"]))
        item = {"nombre": a.nombre, "desc": a.desc or "", "precio": normaliza_precio(a.precio),
                "compact": bool(a.compact)}
        idx = len(sec["items"])
        if a.after:
            idx = busca_item(sec, a.after) + 1
        elif a.posicion is not None:
            idx = max(0, min(a.posicion, len(sec["items"])))
        sec["items"].insert(idx, item)

    elif a.cmd == "price":
        if not a.nombre or not a.precio:
            raise SystemExit("ERROR price: hacen falta --nombre y --precio.")
        sec = seccion(data, a.seccion)
        sec["items"][busca_item(sec, a.nombre)]["precio"] = normaliza_precio(a.precio)

    elif a.cmd == "edit":
        if not a.nombre:
            raise SystemExit("ERROR edit: falta --nombre (el actual).")
        sec = seccion(data, a.seccion)
        k = busca_item(sec, a.nombre)
        it = sec["items"][k]
        if a.nuevonombre: it["nombre"] = a.nuevonombre
        if a.desc is not None: it["desc"] = a.desc
        if a.precio: it["precio"] = normaliza_precio(a.precio)
        if a.compacto == "si": it["compact"] = True
        if a.compacto == "no": it["compact"] = False
        if not any([a.nuevonombre, a.desc is not None, a.precio, a.compacto]):
            raise SystemExit("ERROR edit: no dijiste que cambiar (usa --nuevonombre/--desc/--precio/--compacto).")

    elif a.cmd == "remove":
        if not a.nombre:
            raise SystemExit("ERROR remove: falta --nombre.")
        sec = seccion(data, a.seccion)
        k = busca_item(sec, a.nombre)
        sec["items"].pop(k)

    print(diff_json(antes, data))
    if a.dry_run:
        print("\n(dry-run: no escribi nada)")
        return
    guardar(data)
    render.escribir(HTML, JSON)
    print("\n===== git diff cervezas-camacho.html =====")
    print(git_diff_html())
    print("\nOK: menu-data.json y cervezas-camacho.html actualizados. Revise el diff antes de commitear.")

if __name__ == "__main__":
    main()
