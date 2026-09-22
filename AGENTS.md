# AGENTS.md

Guía de trabajo para agentes de IA en el proyecto **directorio-fm-am**.

## Overview

Script Python que convierte un directorio de estaciones de radio de Guadalajara (ZMG),
escrito en Markdown (`README.md`), en un archivo JSON estructurado
(`radio_guadalajara.json`) con dos listas: `estaciones_fm` y `estaciones_am`.

- `main.py` — script principal y único fuente de lógica.
- `README.md` — documentación pública y fuente de datos de las tablas.
- `pyproject.toml` — proyecto Python (>=3.11) gestionado con `uv`.

## Comandos

- `uv run main.py` — ejecuta la conversión Markdown -> JSON.
- `uv add <paquete>` — añade una dependencia instalable.
- `uv run pytest` — ejecuta los tests.
- `uv run ruff check .` — linter.
- `uv run ruff format .` — formateador.
- `uv lock` / `uv sync` — sincroniza el lockfile y el entorno.

## Convenciones de código

- Python 3.11+, PEP 8, gestionado con `uv` (NUNCA usar pip/pipenv/requirements.txt).
- TODA dependencia debe declararse en `pyproject.toml` y reflejarse en `uv.lock`.
- Docstrings y mensajes de usuario en español; identificadores y nombres de funciones
  en inglés.
- No añadir comentarios al código salvo que se pidan explícitamente.
- Mantener el código fuente ASCII: no emojis en código (sí están permitidos en README, datos y salida).
- Codificación `utf-8` en toda lectura/escritura de archivos y `ensure_ascii=False`
  al serializar JSON.
- No reinventar: usar `pandas.read_html` + `markdown` como ya hace `main.py`.

## Testing

- Usar `pytest`. Añadir tests para `markdown_to_json` y `clean_column_names`.
- Antes de dar por terminado un cambio, ejecutar `uv run pytest` y `uv run ruff check .`.

## Gotchas

- `pd.read_html` devuelve más de una tabla por archivo; el código asume que la primera
  tabla es FM (`estaciones_fm`) y la segunda AM (`estaciones_am`).
- `clean_column_names` pasa las columnas a minúsculas y elimina emojis/símbolos no
  alfanuméricos (necesario porque las cabeceras del README contienen iconos), preservando
  acentos y `ñ` (la regex usa `\w` Unicode, no `[a-z0-9_]`).
- `pd.read_html` recibe el HTML vía `io.StringIO`; en pandas 3.x pasar una cadena
  directamente la trata como ruta de archivo y lanza `FileNotFoundError`.
- Los NaN de pandas deben convertirse a `None` antes de escribir el JSON.
- Si el formato de una tabla cambia (nuevas columnas, más de dos tablas), los tests
  deben actualizarse junto al script.