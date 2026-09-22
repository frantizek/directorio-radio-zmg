"""Regenera las tablas del README a partir de data/estaciones.json.

El README deja de ser la fuente de verdad: las tablas se generan desde el JSON
para que siempre reflejen el estado actual de los datos. Solo se reemplazan las
secciones delimitadas por los marcadores `<!-- TABLA_FM -->` y `<!-- TABLA_AM -->`;
el resto del README (prosa, instrucciones) se conserva tal cual.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "estaciones.json"
README_PATH = ROOT / "README.md"


def format_frecuencia(estacion):
    unidad = "MHz" if estacion["banda"] == "FM" else "kHz"
    return f"{estacion['frecuencia']} {unidad}"


def format_telefono(valor):
    if not valor:
        return ""
    digits = valor[2:] if valor.startswith("52") and len(valor) == 12 else valor
    return digits


def format_whatsapp_numero(valor):
    digits = valor[2:] if valor.startswith("52") and len(valor) == 12 else valor
    return f"{digits[:2]} {digits[2:6]} {digits[6:]}"


def format_whatsapp(contactos):
    whatsapps = [c for c in contactos if c["tipo"] == "whatsapp"]
    if not whatsapps:
        return "`No disponible`"
    partes = []
    for c in whatsapps:
        link = f"[{format_whatsapp_numero(c['valor'])}](http://wa.me/{c['valor']})"
        if c.get("etiqueta"):
            link = f"**{c['etiqueta']}:** {link}"
        if c.get("verificado"):
            link += " ✅"
        partes.append(link)
    return " <br/> ".join(partes)


def format_nombre(estacion):
    nombre = f"**{estacion['nombre']}**"
    programas = estacion.get("programas") or []
    if programas:
        extras = " <br/> ".join(f"▸ *{p['nombre']}*" for p in programas)
        nombre = f"{nombre} <br/> {extras}"
    return nombre


def format_verificado(estacion):
    return "✅" if estacion.get("verificado") else ""


def render_table(estaciones, columna_nombre):
    header = (
        f"| Frecuencia | {columna_nombre} | ☎️ Teléfono Fijo | "
        "Número de WhatsApp | Verificado |"
    )
    sep = (
        "| :--- |:------------------------------------------------| :--- |"
        ":---------------------------------------------------------|:-----------|"
    )
    rows = [header, sep]
    for estacion in estaciones:
        telefono = ""
        for c in estacion.get("contactos") or []:
            if c["tipo"] == "telefono":
                telefono = format_telefono(c["valor"])
                break
        rows.append(
            f"| {format_frecuencia(estacion)} | {format_nombre(estacion)} | "
            f"{telefono} | {format_whatsapp(estacion.get('contactos') or [])} | "
            f"{format_verificado(estacion)} |"
        )
    return "\n".join(rows)


def generate(data):
    fm = [e for e in data["estaciones"] if e["banda"] == "FM"]
    am = [e for e in data["estaciones"] if e["banda"] == "AM"]
    return {
        "TABLA_FM": render_table(fm, "Nombre de la Estación y Programas"),
        "TABLA_AM": render_table(am, "Nombre de la Estación"),
    }


def replace_between(text, marker, content):
    start = f"<!-- {marker} -->"
    end = f"<!-- /{marker} -->"
    if start not in text or end not in text:
        raise ValueError(f"Faltan los marcadores {start} ... {end} en el README")
    before = text.split(start)[0]
    after = text.split(end, 1)[1]
    return before + start + "\n" + content + "\n" + end + after


def update_readme(readme_text, tables):
    text = readme_text
    for marker, content in tables.items():
        text = replace_between(text, marker, content)
    return text


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    readme = README_PATH.read_text(encoding="utf-8")
    README_PATH.write_text(update_readme(readme, generate(data)), encoding="utf-8")
    print(f"README actualizado en '{README_PATH}'.")


if __name__ == "__main__":
    main()
