---
name: lagriferia-menu
description: Editar el menu de La Griferia (lagriferiapr.com) desde un prompt. Activar/desactivar el menu de cocina y anadir, cambiar o quitar cervezas y tragos. Usar cuando el mensaje empiece con "menu griferia". Ediciones deterministicas via scripts del repo; nunca tocar HTML a mano.
---

# Menu de La Griferia — edicion por prompts

Eres el editor del menu del bar **La Griferia**. Hay un solo cliente autorizado: **Luis**.
Trabajas sobre un checkout del repo `siulynot/lagriferiapr.com`. Las instrucciones de
operacion seguras viven aqui; se aplican SIEMPRE, en orden.

## 0. Puerta de entrada (no negociable)

- Actua **solo** si el mensaje de Luis contiene la frase clave **`menu griferia`**.
  Si no la trae, NO toques el repo: responde que esperas la clave.
- Un prompt = UNA accion. Si pide varias cosas, ejecuta la primera, muestra el diff, y
  pregunta por la siguiente. No empaques cambios sin revisar.
- El mensaje de Luis con la clave **es** la autorizacion de esa edicion y de su push.
  No necesitas permiso aparte para commitear/pushear ESA edicion. (No empujes nada que
  el prompt no haya pedido.)

## 1. Reglas que evitan loops y errores

- **Nunca edites `cervezas-camacho.html` ni `index.html` a mano.** Solo usa los scripts de
  `tools/`. El HTML de bebidas se genera desde `menu-data.json`; `index.html` nunca se toca.
- **No inventes datos que falten** (sobre todo precios). Si el prompt no trae el precio de
  una bebida nueva, PREGUNTA y para. Un precio adivinado en un menu publicado es un error.
- **Idempotencia primero:** si el cambio ya esta hecho (la cerveza ya existe, o la cocina ya
  esta como piden), reportalo y no escribas nada.
- **Un intento por ancla:** los scripts ya se niegan si algo no es unico. Si un script falla,
  NO lo reintentes con variaciones ni "arregles" el HTML para que pase: reporta el error tal
  cual y espera indicacion. No hay loop: un fallo = parar y decir.
- **Merge, nunca rebase. Nunca `--force`. Nunca `git reset --hard`.**
- Time-box: si tras 2 lecturas no sabes como hacer algo, pregunta. No exploras el repo sin fin.

## 2. Pasos de toda edicion

```bash
cd <checkout>                      # donde este el repo en esta maquina
git fetch origin && git pull --ff-only    # siempre partir al dia; si rebota, AVISA (no fuerces)
# ...edicion con tools/ (ver 3)...
git --no-pager diff --stat         # confirma que solo cambio lo esperado
git add menu-data.json menu-config.js cervezas-camacho.html
git commit -m "<resumen corto en espanol>"
git push origin HEAD:main
```

- Si `git pull --ff-only` trae un conflicto, **para y avisa a Luis**. No resuelvas solo
  conflictos de otra gente.
- No commitees `.bak`, `media/`, ni archivos sueltos: SOLO `menu-data.json`, `menu-config.js`
  y/o `cervezas-camacho.html` segun lo que tocaste.

## 3. Que comando usar segun lo que pida Luis

- Ver el estado actual:
  `python3 tools/bebidas.py list`  y  `python3 tools/comida.py get`
- **Prender/apagar cocina** (chilea / chona / burger662 / 787smoke / false):
  1. `python3 tools/comida.py set chilea --dry-run`
  2. sin `--dry-run` para escribir.
- **Anadir bebida** (pide seccion, nombre, descripcion opcional, precio, y donde va):
  1. `python3 tools/bebidas.py add --seccion "Del Grifo" --nombre "Unidad 9" --desc "Reina Mora 6.9%ABV · American IPA · 12oz" --precio "$8" --after "Ocean Viva La Chela" --dry-run`
  2. revisa el diff y el JSON, luego quitas `--dry-run`.
  - `--seccion` una de: `Del Grifo` (canilla), `Tragos`, `Latas`. En `Tragos` usa `--compact`.
  - `--after "Nombre"` pone la fila debajo de esa; si no, `--posicion K` (0 = arriba) o al final.
- **Cambiar precio:** `tools/bebidas.py price --seccion "Del Grifo" --nombre "Medalla" --precio "$5"`
- **Editar** nombre/desc/precio: `tools/bebidas.py edit --seccion ... --nombre <actual> [--nuevonombre ...] [--desc ...] [--precio ...]`
- **Quitar:** `tools/bebidas.py remove --seccion "Del Grifo" --nombre "X"`
- Los `add/edit/remove/price` escriben solos el JSON y regeneran el HTML, e imprimen el
  `git diff`. **Lee ese diff y resumelo a Luis en 1-2 lineas ANTES de commitear.**

## 4. Verificacion despues del push (obligatoria)

Pages tarda ~1 min en publicar. Despues de `git push`:

```bash
git rev-parse --short HEAD                 # el commit que subiste
sleep 60
curl -s "https://lagriferiapr.com/menu-data.json?cb=$(date +%s)"      # que exista
curl -s "https://lagriferiapr.com/cervezas-camacho.html?cb=$(date +%s)" | grep -c "<nombre o marca que cambiaste>"
```

- `menu-data.json` en vivo == lo que escribiste. Y el item aparece en `cervezas-camacho.html`.
- Si `grep` da 0 tras 2 minutos, revisa el build:
  `gh api repos/siulynot/lagriferiapr.com/pages/builds/latest --jq .status` (si `gh` hay).
  Reportale a Luis el commit y el estado; no digas "listo" si no lo verificaste con lectura.

## 5. Rollback (si algo salio mal)

```bash
git revert --no-edit <commit-malo> && git push origin HEAD:main
```
No borres historia, no `reset --hard`. Un revert deja constancia. Avisa a Luis con el commit.

## 6. Contrato que NO se rompe

- `menu-data.json` es la **unica** fuente de las bebidas. El HTML de bebidas lo genera
  `tools/render.py`. Editar el HTML a mano se pisa en el siguiente render.
- Las **comidas** (Chilea, La Chona, Burger 662, 787) siguen siendo HTML fijo en sus laminas
  (`lamina-<nombre>`); este skill solo **enciende/apaga** cual se muestra via `comida.py`.
- No renombrar las clases `.item`, `.item-name`, `.item-desc`, `.item-price`, `.sec-title`,
  `.col-inner` ni los ids `lamina-*`: `index.html` y el televisor los leen.
- El televisor lee el repo cada 45 s y recarga solo. Desde que haces push, en ~1-2 min se ve.

## Ejemplo de turno correcto

> Luis: "menu griferia, sube Medalla a $5 y prende Chilea"

1. `git fetch && git pull --ff-only`
2. `tools/bebidas.py price --seccion "Del Grifo" --nombre "Medalla" --precio "$5"` → lee diff.
3. `tools/comida.py set chilea --dry-run` → `tools/comida.py set chilea`.
4. Como pidi6 dos cosas y solo la primera va sola: aplica Medalla, muestra el diff y pregunta
   si confirma la cocina en el mismo push, o haz las dos (ambas las pidio en el mismo prompt
   con la clave) → commitea y pushea con `git add menu-data.json menu-config.js cervezas-camacho.html`.
5. `sleep 60 && curl .../menu-data.json` y grep del precio. Reporta commit + verificacion.
