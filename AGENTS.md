# AGENTS.md

Guía de trabajo para agentes de IA en el proyecto **directorio-fm-am**.

## Overview

Directorio web de estaciones de radio de Guadalajara (ZMG), México. Combina:

- **`data/estaciones.json`** — fuente de verdad. Modelo: estación (`id`, `banda`, `frecuencia`, `nombre`, `verificado`) con `contactos[]` y `programas[]`. Cada contacto tiene `tipo`, `valor` y opcionalmente `etiqueta`/`verificado`. Cada programa tiene `nombre`, `horario`, `dias`, `locutores` y sus propios `contactos`.
- **Frontend estático** en la raíz (`index.html`, `css/`, `js/`) — SPA con Alpine.js (auto-hospedado en `js/vendor/`), i18n es/en (`js/i18n.js`), y edición que guarda vía pull request usando la API de GitHub (`js/github.js`).
- **Scripts Python** — `scripts/migrate.py` (migración única README → JSON) y `scripts/generate_readme.py` (JSON → README).
- **`pyproject.toml`** — proyecto Python (>=3.11) gestionado con `uv`, sin dependencias de runtime.

## Comandos

- `uv run python scripts/migrate.py` — migra las tablas del README a `data/estaciones.json`.
- `uv run python scripts/generate_readme.py` — regenera las tablas del README desde el JSON.
- `uv run pytest` — ejecuta los tests.
- `uv run ruff check .` — linter.
- `uv run ruff format .` — formateador.
- `node --check js/*.js` — verifica sintaxis del frontend.
- `python -m http.server 8000` — sirve la web localmente (http://localhost:8000).

## Convenciones de código

- Python 3.11+, PEP 8, gestionado con `uv` (NUNCA usar pip/pipenv/requirements.txt).
- TODA dependencia debe declararse en `pyproject.toml` y reflejarse en `uv.lock`.
- Docstrings y mensajes de usuario en español; identificadores y nombres de funciones en inglés.
- No añadir comentarios al código salvo que se pidan explícitamente.
- Mantener el código fuente ASCII: no emojis en código (sí están permitidos en README, datos y salida).
- Codificación `utf-8` en toda lectura/escritura de archivos y `ensure_ascii=False` al serializar JSON.
- Frontend: JS estilo ES5 (`var`, `function`), `"use strict"`, sin build step, sin dependencias externas (Alpine auto-hospedado). Toda etiqueta de UI vía `t()` de `js/i18n.js`.

## Testing

- Usar `pytest` para los scripts Python. Añadir tests para `migrate` y `generate_readme`.
- Verificar sintaxis del frontend con `node --check js/*.js`.
- Antes de dar por terminado un cambio, ejecutar `uv run pytest` y `uv run ruff check .`.

## Gotchas

- `data/estaciones.json` es la fuente de verdad; el README se regenera con `generate_readme.py` (no editar las tablas a mano para datos).
- Teléfonos y WhatsApp se guardan en E.164 (`52` + 10 dígitos); `dias` de programas en ISO (1=Lunes ... 7=Domingo).
- Tipos de contacto válidos: `telefono`, `whatsapp`, `telegram`, `instagram`, `facebook`, `x`, `threads`, `tiktok`, `youtube`, `tunein`, `iheart`, `web`, `email`.
- El frontend normaliza los datos al guardar (`normalizeStations` en `js/app.js`): allowlist de tipos, E.164, días válidos 1-7, y rechaza frecuencias duplicadas en la misma banda.
- El guardado web crea rama + commit + PR (`saveChanges` en `js/github.js`); requiere `CONFIG.owner` configurado en `js/config.js` y un PAT con permisos Contents y Pull requests.
- `index.html` tiene una CSP estricta (`script-src 'self' 'unsafe-eval'`): Alpine debe vivir en `js/vendor/` y las llamadas a la API solo a `api.github.com`. El `'unsafe-eval'` es obligatorio porque Alpine evalúa sus expresiones con `eval`/`new Function`; sin él la página no renderiza nada.
- Si cambia el modelo de datos, actualizar a la vez: `scripts/migrate.py`, `scripts/generate_readme.py`, `js/app.js` (`normalizeStations`), los tests y la documentación.