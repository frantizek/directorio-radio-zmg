"""Regenera las tablas del README a partir de data/estaciones.json.

El README deja de ser la fuente de verdad: se genera desde el JSON para que
siempre refleje el estado actual de los datos.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "estaciones.json"
README_PATH = ROOT / "README.md"

HEADER = """# Lista de Estaciones de Radio en Guadalajara, México (AM y FM)

A continuación se presenta una lista de las principales estaciones de radio en la Zona Metropolitana de Guadalajara (ZMG), con su frecuencia, nombre, teléfono fijo, enlace de WhatsApp y estado de verificación.

**Nota:** Los números pueden cambiar. Se recomienda verificar en los sitios web oficiales para la información más reciente.

---
"""


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
    partes = [HEADER]
    partes.append("## Estaciones de FM (Frecuencia Modulada)\n")
    partes.append(render_table(fm, "Nombre de la Estación y Programas"))
    partes.append("\n---\n")
    partes.append("## Estaciones de AM (Amplitud Modulada)\n")
    partes.append(render_table(am, "Nombre de la Estación"))
    return "\n".join(partes) + "\n"


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    README_PATH.write_text(generate(data), encoding="utf-8")
    print(f"README regenerado en '{README_PATH}'.")


if __name__ == "__main__":
    main()
