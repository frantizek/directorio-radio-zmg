"""Normalización y persistencia de las estaciones de radio.

Centraliza la lógica de validación del modelo de datos (la misma que antes vivía
en el frontend) y la lectura/escritura de `data/estaciones.json`. Lo usan el
servidor de administración local (`scripts/admin_server.py`) y los tests.
"""

import json
import re
from pathlib import Path

from scripts.generate_readme import generate, update_readme

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "estaciones.json"
README_PATH = ROOT / "README.md"

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

MAX_LEN = {
    "frecuencia": 20,
    "nombre": 200,
    "valor": 500,
    "etiqueta": 100,
    "programa": 200,
    "horario": 200,
    "locutor": 200,
}


def _clean(value, max_len):
    return str(value or "").strip()[:max_len]


def normalize_contact(contacto):
    """Normaliza un contacto: allowlist de tipos y E.164 para teléfono/WhatsApp."""
    if not isinstance(contacto, dict):
        return None
    tipo = contacto.get("tipo")
    if tipo not in CONTACT_TYPES:
        tipo = "whatsapp"
    valor = _clean(contacto.get("valor"), MAX_LEN["valor"])
    if tipo in ("telefono", "whatsapp"):
        digits = re.sub(r"\D", "", valor)
        if len(digits) == 10:
            valor = "52" + digits
        elif len(digits) == 12 and digits.startswith("52"):
            valor = digits
        else:
            valor = digits
    if not valor:
        return None
    out = {"tipo": tipo, "valor": valor}
    etiqueta = _clean(contacto.get("etiqueta"), MAX_LEN["etiqueta"])
    if etiqueta:
        out["etiqueta"] = etiqueta
    if contacto.get("verificado"):
        out["verificado"] = True
    return out


def normalize_programa(programa):
    """Normaliza un programa: nombre, horario, días 1-7, locutores y contactos."""
    if not isinstance(programa, dict):
        return None
    nombre = _clean(programa.get("nombre"), MAX_LEN["programa"])
    if not nombre:
        return None
    horario = _clean(programa.get("horario"), MAX_LEN["horario"]) or None
    dias = sorted(
        {
            d
            for d in (programa.get("dias") or [])
            if isinstance(d, int) and 1 <= d <= 7
        }
    )
    locutores = [
        _clean(x, MAX_LEN["locutor"]) for x in (programa.get("locutores") or [])
    ]
    locutores = [x for x in locutores if x]
    contactos = [
        c
        for c in (normalize_contact(c) for c in (programa.get("contactos") or []))
        if c
    ]
    return {
        "nombre": nombre,
        "horario": horario,
        "dias": dias,
        "locutores": locutores,
        "contactos": contactos,
    }


def normalize_estacion(estacion):
    """Normaliza una estación y calcula su id (banda-frecuencia)."""
    if not isinstance(estacion, dict):
        return None
    banda = _clean(estacion.get("banda"), 2).upper()
    if banda not in ("FM", "AM"):
        banda = "FM"
    frecuencia = _clean(estacion.get("frecuencia"), MAX_LEN["frecuencia"])
    nombre = _clean(estacion.get("nombre"), MAX_LEN["nombre"])
    if not nombre or not frecuencia:
        return None
    contactos = [
        c
        for c in (normalize_contact(c) for c in (estacion.get("contactos") or []))
        if c
    ]
    programas = [
        p
        for p in (normalize_programa(p) for p in (estacion.get("programas") or []))
        if p
    ]
    return {
        "id": f"{banda.lower()}-{frecuencia}",
        "banda": banda,
        "frecuencia": frecuencia,
        "nombre": nombre,
        "verificado": bool(estacion.get("verificado")),
        "contactos": contactos,
        "programas": programas,
    }


def normalize_estaciones(estaciones):
    """Normaliza una lista completa, descartando entradas inválidas."""
    return [e for e in (normalize_estacion(e) for e in estaciones) if e]


def find_duplicate(estaciones):
    """Devuelve el id repetido si dos estaciones comparten banda+frecuencia."""
    seen = set()
    for estacion in estaciones:
        if estacion["id"] in seen:
            return estacion["id"]
        seen.add(estacion["id"])
    return None


def _sort_key(estacion):
    banda_order = 0 if estacion["banda"] == "FM" else 1
    try:
        frecuencia = float(estacion["frecuencia"])
    except ValueError:
        frecuencia = float("inf")
    return (banda_order, frecuencia)


def load_estaciones(path=DATA_PATH):
    """Lee la lista de estaciones desde el JSON."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("estaciones", [])


def save_estaciones(estaciones, path=DATA_PATH, readme_path=README_PATH):
    """Escribe el JSON ordenado y regenera el README para mantenerlos en sincronía."""
    estaciones = sorted(estaciones, key=_sort_key)
    path.write_text(
        json.dumps({"estaciones": estaciones}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    readme = readme_path.read_text(encoding="utf-8")
    readme_path.write_text(
        update_readme(readme, generate({"estaciones": estaciones})),
        encoding="utf-8",
    )