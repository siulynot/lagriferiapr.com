#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prende/apaga el menu de cocina del televisor y la web (menu-config.js).

Escribe la linea window.HAY_COMIDA. Un solo valor a la vez:
  chilea | chona | burger662 | 787smoke   (con comillas)
  false                                   (SIN comillas: no hay comida, solo cervezas)

Se niega ante cualquier otra cosa (erratas) para no apagar la comida por error
ni anunciar un popup que no existe.

Comandos:
  get
  set <valor>  [--dry-run]
"""
import sys, os, re, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = os.path.join(ROOT, "menu-config.js")
VALIDAS = {"chilea", "chona", "burger662", "787smoke"}

def nuevo_texto(valor):
    s = open(CFG, encoding="utf-8").read()
    if valor == "false":
        reemplazo = "window.HAY_COMIDA = false;"
    elif valor in VALIDAS:
        reemplazo = "window.HAY_COMIDA = '%s';" % valor
    else:
        raise SystemExit("ERROR valor: '%s' no es conocido. Validos: %s, false" % (valor, ", ".join(sorted(VALIDAS))))
    pat = re.compile(r"window\.HAY_COMIDA\s*=\s*['\"]?[A-Za-z0-9]+['\"]?;")
    n = len(pat.findall(s))
    if n != 1:
        raise SystemExit("ERROR: hay %d lineas HAY_COMIDA, deberia haber 1. Reviso a mano antes de tocar." % n)
    return pat.sub(reemplazo, s, count=1)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get")
    p = sub.add_parser("set"); p.add_argument("valor"); p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    s = open(CFG, encoding="utf-8").read()
    m = re.search(r"window\.HAY_COMIDA\s*=\s*['\"]?([A-Za-z0-9]+)['\"]?", s)
    actual = m.group(1) if m else "?"

    if a.cmd == "get":
        print("HAY_COMIDA =", actual)
        return

    if actual == a.valor:
        print("Ya esta en '%s'. No cambio nada." % a.valor)
        return
    nuevo = nuevo_texto(a.valor)
    linea = [l for l in nuevo.splitlines() if "HAY_COMIDA" in l and not l.strip().startswith("*")][0]
    print("Antes: %s\nDespues: %s" % (actual, a.valor))
    if a.dry_run:
        print("(dry-run: no escribi)"); return
    open(CFG, "w", encoding="utf-8").write(nuevo)
    print("OK: menu-config.js ->", linea.strip())

if __name__ == "__main__":
    main()
