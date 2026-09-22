"""Migra las tablas del README al nuevo modelo de datos en data/estaciones.json.

El nuevo modelo estructura cada estación con datos principales, una lista de
contactos (teléfono, WhatsApp, redes sociales, web, email, etc.) y una lista de
programas que pueden tener sus propios contactos, horario, días y locutores.

Este script es de migración única: después de la primera ejecución, la fuente de
verdad es data/estaciones.json y el README se regenera con generate_readme.py.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
OUTPUT_PATH = ROOT / "data" / "estaciones.json"

CONTACT_TYPES = (
    "telefono",
    "whatsapp",
    "telegram",
    "instagram",
    "facebook",
    "x",
    "threads",
    "tiktok",
    "youtube",
    "tunein",
    "iheart",
    "web",
    "email",
)


def parse_markdown_tables(md_text):
    """Extrae las tablas markdown como listas de filas de celdas crudas."""
    tables = []
    current = None
    for line in md_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if current is not None:
                tables.append(current)
                current = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        if current is None:
            current = []
        current.append(cells)
    if current is not None:
        tables.append(current)
    return tables


def parse_frecuencia(cell):
    """Devuelve (banda, frecuencia) a partir de '104.3 MHz' o '580 kHz'."""
    match = re.match(r"([\d.]+)\s*(MHz|kHz)", cell)
    if not match:
        return None, cell
    numero, unidad = match.groups()
    banda = "FM" if unidad == "MHz" else "AM"
    return banda, numero


def parse_nombre(cell):
    """Separa el nombre de la estación de sus programas.

    '**Radio UdeG** <br/> ▸ *El Expreso de las Diez*' -> ('Radio UdeG', ['El Expreso de las Diez'])
    """
    parts = [p.strip() for p in cell.split("<br/>")]
    nombre = parts[0].strip().strip("*").strip()
    programas = []
    for part in parts[1:]:
        programa = part.strip().strip("▸").strip().strip("*").strip()
        if programa:
            programas.append(programa)
    return nombre, programas


def parse_telefono(cell):
    """Normaliza un teléfono a E.164 ('33 1716 0006' -> '523317160006') o None."""
    cell = cell.strip()
    if not cell:
        return None
    digits = re.sub(r"\D", "", cell)
    if not digits:
        return None
    if len(digits) == 10:
        return "52" + digits
    return digits


def parse_whatsapp(cell):
    """Parsea la celda de WhatsApp y devuelve una lista de contactos.

    Soporta 'No disponible', un enlace simple y entradas etiquetadas como
    '**General:** [33 2053 6975](http://wa.me/523320536975) ✅'.
    """
    cell = cell.strip()
    if not cell or cell == "No disponible":
        return []
    contactos = []
    for part in cell.split("<br/>"):
        part = part.strip()
        if not part:
            continue
        etiqueta = None
        label_match = re.match(r"\*\*(.+?):\*\*\s*(.*)", part)
        if label_match:
            etiqueta = label_match.group(1).strip()
            part = label_match.group(2).strip()
        link_match = re.search(r"\[[^\]]*\]\(http://wa\.me/(\d+)\)", part)
        if not link_match:
            continue
        contacto = {"tipo": "whatsapp", "valor": link_match.group(1)}
        if etiqueta:
            contacto["etiqueta"] = etiqueta
        if "✅" in part:
            contacto["verificado"] = True
        contactos.append(contacto)
    return contactos


def parse_row(row):
    """Convierte una fila de tabla en una estación del nuevo modelo."""
    frecuencia_cell = row[0]
    nombre_cell = row[1]
    telefono_cell = row[2] if len(row) > 2 else ""
    whatsapp_cell = row[3] if len(row) > 3 else ""
    verificado_cell = row[4] if len(row) > 4 else ""

    banda, frecuencia = parse_frecuencia(frecuencia_cell)
    if not banda:
        return None
    nombre, programas_nombres = parse_nombre(nombre_cell)

    contactos = []
    telefono = parse_telefono(telefono_cell)
    if telefono:
        contactos.append({"tipo": "telefono", "valor": telefono})

    programas = [
        {
            "nombre": nombre_programa,
            "horario": None,
            "dias": [],
            "locutores": [],
            "contactos": [],
        }
        for nombre_programa in programas_nombres
    ]

    for contacto in parse_whatsapp(whatsapp_cell):
        etiqueta = (contacto.get("etiqueta") or "").lower()
        if etiqueta == "programa" and programas:
            programas[0]["contactos"].append(contacto)
        else:
            contactos.append(contacto)

    return {
        "id": f"{banda.lower()}-{frecuencia}",
        "banda": banda,
        "frecuencia": frecuencia,
        "nombre": nombre,
        "verificado": verificado_cell.strip() == "✅",
        "contactos": contactos,
        "programas": programas,
    }


def migrate(md_text):
    """Convierte el texto markdown del README en el diccionario de estaciones."""
    tables = parse_markdown_tables(md_text)
    if len(tables) < 2:
        raise ValueError("Se esperaban al menos dos tablas (FM y AM) en el README")
    estaciones = []
    for table in tables[:2]:
        for row in table[1:]:
            estacion = parse_row(row)
            if estacion:
                estaciones.append(estacion)
    return {"estaciones": estaciones}


def main():
    md_text = README_PATH.read_text(encoding="utf-8")
    data = migrate(md_text)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    fm = sum(1 for e in data["estaciones"] if e["banda"] == "FM")
    am = sum(1 for e in data["estaciones"] if e["banda"] == "AM")
    print(f"Migradas {fm} estaciones FM y {am} AM a '{OUTPUT_PATH}'.")


if __name__ == "__main__":
    main()
