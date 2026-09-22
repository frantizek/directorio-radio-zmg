from scripts.generate_readme import (
    format_frecuencia,
    format_nombre,
    format_telefono,
    format_whatsapp,
    generate,
    replace_between,
    update_readme,
)

DATA_SAMPLE = {
    "estaciones": [
        {
            "id": "fm-88.7",
            "banda": "FM",
            "frecuencia": "88.7",
            "nombre": "ArrobaFM",
            "verificado": True,
            "contactos": [{"tipo": "telefono", "valor": "523338250887"}],
            "programas": [],
        },
        {
            "id": "fm-104.3",
            "banda": "FM",
            "frecuencia": "104.3",
            "nombre": "Radio UdeG",
            "verificado": True,
            "contactos": [
                {"tipo": "telefono", "valor": "523317160006"},
                {
                    "tipo": "whatsapp",
                    "valor": "523320536975",
                    "etiqueta": "General",
                    "verificado": True,
                },
            ],
            "programas": [
                {
                    "nombre": "El Expreso de las Diez",
                    "horario": None,
                    "dias": [],
                    "locutores": [],
                    "contactos": [],
                }
            ],
        },
        {
            "id": "am-580",
            "banda": "AM",
            "frecuencia": "580",
            "nombre": "Radio 580",
            "verificado": False,
            "contactos": [{"tipo": "whatsapp", "valor": "523331221190"}],
            "programas": [],
        },
    ]
}

README_SAMPLE = """# Directorio de Radio ZMG

Prosa que no debe tocarse.

## Estaciones de FM (Frecuencia Modulada)

<!-- TABLA_FM -->
| vieja |
<!-- /TABLA_FM -->

## Estaciones de AM (Amplitud Modulada)

<!-- TABLA_AM -->
| vieja |
<!-- /TABLA_AM -->
"""


def test_format_frecuencia():
    assert format_frecuencia({"banda": "FM", "frecuencia": "88.7"}) == "88.7 MHz"
    assert format_frecuencia({"banda": "AM", "frecuencia": "580"}) == "580 kHz"


def test_format_telefono():
    assert format_telefono("523338250887") == "3338250887"
    assert format_telefono("") == ""


def test_format_whatsapp_simple():
    contactos = [{"tipo": "whatsapp", "valor": "523319727663"}]
    assert format_whatsapp(contactos) == "[33 1972 7663](http://wa.me/523319727663)"


def test_format_whatsapp_no_disponible():
    assert format_whatsapp([]) == "`No disponible`"


def test_format_whatsapp_labeled():
    contactos = [
        {
            "tipo": "whatsapp",
            "valor": "523320536975",
            "etiqueta": "General",
            "verificado": True,
        }
    ]
    assert (
        format_whatsapp(contactos)
        == "**General:** [33 2053 6975](http://wa.me/523320536975) ✅"
    )


def test_format_nombre_with_program():
    estacion = {
        "nombre": "Radio UdeG",
        "programas": [{"nombre": "El Expreso de las Diez"}],
    }
    assert format_nombre(estacion) == "**Radio UdeG** <br/> ▸ *El Expreso de las Diez*"


def test_generate_returns_tables():
    tables = generate(DATA_SAMPLE)
    assert set(tables.keys()) == {"TABLA_FM", "TABLA_AM"}
    assert "**ArrobaFM**" in tables["TABLA_FM"]
    assert "**Radio UdeG** <br/> ▸ *El Expreso de las Diez*" in tables["TABLA_FM"]
    assert (
        "**General:** [33 2053 6975](http://wa.me/523320536975) ✅"
        in tables["TABLA_FM"]
    )
    assert "**Radio 580**" in tables["TABLA_AM"]


def test_update_readme_preserves_prose():
    tables = generate(DATA_SAMPLE)
    updated = update_readme(README_SAMPLE, tables)
    assert "Prosa que no debe tocarse." in updated
    assert "**ArrobaFM**" in updated
    assert "**Radio 580**" in updated
    assert "| vieja |" not in updated


def test_replace_between_raises_without_markers():
    try:
        replace_between("sin marcadores", "TABLA_FM", "x")
    except ValueError:
        return
    raise AssertionError("Debería lanzar ValueError sin marcadores")
