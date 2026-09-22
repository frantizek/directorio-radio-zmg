import json

from scripts.estaciones import (
    find_duplicate,
    normalize_contact,
    normalize_estacion,
    normalize_estaciones,
    normalize_programa,
    save_estaciones,
)

README_WITH_MARKERS = """# Directorio

<!-- TABLA_FM -->
| vieja |
<!-- /TABLA_FM -->

<!-- TABLA_AM -->
| vieja |
<!-- /TABLA_AM -->
"""


def test_normalize_contact_e164():
    assert normalize_contact({"tipo": "telefono", "valor": "33 1716 0006"}) == {
        "tipo": "telefono",
        "valor": "523317160006",
    }
    assert normalize_contact({"tipo": "whatsapp", "valor": "523319727663"}) == {
        "tipo": "whatsapp",
        "valor": "523319727663",
    }


def test_normalize_contact_unknown_type_defaults_to_whatsapp():
    assert normalize_contact({"tipo": "fax", "valor": "3312345678"}) == {
        "tipo": "whatsapp",
        "valor": "523312345678",
    }


def test_normalize_contact_empty_returns_none():
    assert normalize_contact({"tipo": "web", "valor": "  "}) is None
    assert normalize_contact(None) is None


def test_normalize_contact_keeps_etiqueta_and_verificado():
    out = normalize_contact(
        {"tipo": "whatsapp", "valor": "523319727663", "etiqueta": "General", "verificado": True}
    )
    assert out["etiqueta"] == "General"
    assert out["verificado"] is True


def test_normalize_programa_filters_days_and_locutores():
    out = normalize_programa(
        {
            "nombre": "El Expreso",
            "horario": "10:00 - 12:00",
            "dias": [1, 5, 9, "x", 3],
            "locutores": ["Ana", "  ", "Luis"],
            "contactos": [{"tipo": "whatsapp", "valor": "523319727663"}],
        }
    )
    assert out["dias"] == [1, 3, 5]
    assert out["locutores"] == ["Ana", "Luis"]
    assert out["contactos"] == [{"tipo": "whatsapp", "valor": "523319727663"}]


def test_normalize_programa_without_name_returns_none():
    assert normalize_programa({"nombre": "  "}) is None


def test_normalize_estacion_computes_id():
    out = normalize_estacion(
        {"banda": "fm", "frecuencia": "104.3", "nombre": "Radio UdeG", "verificado": True}
    )
    assert out["id"] == "fm-104.3"
    assert out["banda"] == "FM"
    assert out["verificado"] is True


def test_normalize_estacion_incomplete_returns_none():
    assert normalize_estacion({"banda": "FM", "frecuencia": "", "nombre": "X"}) is None
    assert normalize_estacion({"banda": "FM", "frecuencia": "88.7", "nombre": ""}) is None


def test_normalize_estaciones_filters_invalid():
    out = normalize_estaciones(
        [
            {"banda": "FM", "frecuencia": "88.7", "nombre": "ArrobaFM"},
            {"banda": "AM", "frecuencia": "", "nombre": "Inválida"},
        ]
    )
    assert len(out) == 1
    assert out[0]["id"] == "fm-88.7"


def test_find_duplicate():
    estaciones = [
        {"id": "fm-88.7"},
        {"id": "fm-104.3"},
        {"id": "fm-88.7"},
    ]
    assert find_duplicate(estaciones) == "fm-88.7"
    assert find_duplicate(estaciones[:2]) is None


def test_save_estaciones_writes_json_and_readme(tmp_path):
    data_path = tmp_path / "estaciones.json"
    readme_path = tmp_path / "README.md"
    readme_path.write_text(README_WITH_MARKERS, encoding="utf-8")
    estaciones = [
        {"id": "fm-88.7", "banda": "FM", "frecuencia": "88.7", "nombre": "ArrobaFM",
         "verificado": True, "contactos": [], "programas": []}
    ]
    save_estaciones(estaciones, data_path, readme_path)

    data = json.loads(data_path.read_text(encoding="utf-8"))
    assert data["estaciones"][0]["nombre"] == "ArrobaFM"

    readme = readme_path.read_text(encoding="utf-8")
    assert "**ArrobaFM**" in readme
    assert "| vieja |" not in readme


def test_save_estaciones_sorts_by_band_and_frequency(tmp_path):
    data_path = tmp_path / "estaciones.json"
    readme_path = tmp_path / "README.md"
    readme_path.write_text(README_WITH_MARKERS, encoding="utf-8")
    estaciones = [
        {"id": "am-580", "banda": "AM", "frecuencia": "580", "nombre": "Radio 580",
         "verificado": False, "contactos": [], "programas": []},
        {"id": "fm-104.3", "banda": "FM", "frecuencia": "104.3", "nombre": "Radio UdeG",
         "verificado": False, "contactos": [], "programas": []},
        {"id": "fm-88.7", "banda": "FM", "frecuencia": "88.7", "nombre": "ArrobaFM",
         "verificado": False, "contactos": [], "programas": []},
    ]
    save_estaciones(estaciones, data_path, readme_path)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    ids = [e["id"] for e in data["estaciones"]]
    assert ids == ["fm-88.7", "fm-104.3", "am-580"]