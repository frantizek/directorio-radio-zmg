import json

from scripts.migrate import (
    migrate,
    parse_frecuencia,
    parse_markdown_tables,
    parse_nombre,
    parse_telefono,
    parse_whatsapp,
)

MD_SAMPLE = """# Lista de Estaciones de Radio

## FM

| Frecuencia | Nombre de la Estación y Programas | ☎️ Teléfono Fijo | Número de WhatsApp | Verificado |
| :--- |:------------------------------------------------| :--- |:---------------------------------------------------------|:-----------|
| 88.7 MHz | **ArrobaFM** | 3338250887 | `No disponible` | ✅ |
| 104.3 MHz| **Radio UdeG** <br/> ▸ *El Expreso de las Diez* | 33 1716 0006 | **General:** [33 2053 6975](http://wa.me/523320536975) ✅ <br/> **Programa:** [33 2030 3232](http://wa.me/523320303232) ✅ | ✅ |

## AM

| Frecuencia | Nombre de la Estación | ☎️ Teléfono Fijo | Número de WhatsApp | Verificado |
| :--- | :--- | :--- | :--- | :--- |
| 580 kHz | **Radio 580** | | [33 3122 1190](http://wa.me/523331221190) | |
"""


def test_parse_markdown_tables_extracts_two_tables():
    tables = parse_markdown_tables(MD_SAMPLE)
    assert len(tables) == 2
    assert tables[0][0][0] == "Frecuencia"
    assert tables[1][0][0] == "Frecuencia"


def test_parse_frecuencia():
    assert parse_frecuencia("104.3 MHz") == ("FM", "104.3")
    assert parse_frecuencia("580 kHz") == ("AM", "580")


def test_parse_nombre_with_program():
    nombre, programas = parse_nombre("**Radio UdeG** <br/> ▸ *El Expreso de las Diez*")
    assert nombre == "Radio UdeG"
    assert programas == ["El Expreso de las Diez"]


def test_parse_nombre_simple():
    assert parse_nombre("**ArrobaFM**") == ("ArrobaFM", [])


def test_parse_telefono_e164():
    assert parse_telefono("33 1716 0006") == "523317160006"
    assert parse_telefono("3338250887") == "523338250887"
    assert parse_telefono("") is None


def test_parse_whatsapp_simple():
    contactos = parse_whatsapp("[33 1972 7663](http://wa.me/523319727663)")
    assert contactos == [{"tipo": "whatsapp", "valor": "523319727663"}]


def test_parse_whatsapp_no_disponible():
    assert parse_whatsapp("`No disponible`") == []
    assert parse_whatsapp("") == []


def test_parse_whatsapp_labeled():
    cell = (
        "**General:** [33 2053 6975](http://wa.me/523320536975) ✅ "
        "<br/> **Programa:** [33 2030 3232](http://wa.me/523320303232) ✅"
    )
    contactos = parse_whatsapp(cell)
    assert contactos[0] == {
        "tipo": "whatsapp",
        "valor": "523320536975",
        "etiqueta": "General",
        "verificado": True,
    }
    assert contactos[1]["etiqueta"] == "Programa"


def test_migrate_creates_full_model():
    data = migrate(MD_SAMPLE)
    assert set(data.keys()) == {"estaciones"}
    assert len(data["estaciones"]) == 3

    arroba = data["estaciones"][0]
    assert arroba["id"] == "fm-88.7"
    assert arroba["banda"] == "FM"
    assert arroba["frecuencia"] == "88.7"
    assert arroba["verificado"] is True
    assert arroba["contactos"] == [{"tipo": "telefono", "valor": "523338250887"}]
    assert arroba["programas"] == []

    udeg = data["estaciones"][1]
    assert udeg["nombre"] == "Radio UdeG"
    assert [c.get("etiqueta") for c in udeg["contactos"]] == [None, "General"]
    assert udeg["programas"][0]["nombre"] == "El Expreso de las Diez"
    assert udeg["programas"][0]["contactos"][0]["etiqueta"] == "Programa"
    assert udeg["programas"][0]["horario"] is None
    assert udeg["programas"][0]["dias"] == []
    assert udeg["programas"][0]["locutores"] == []

    radio580 = data["estaciones"][2]
    assert radio580["id"] == "am-580"
    assert radio580["banda"] == "AM"
    assert radio580["verificado"] is False
    assert radio580["contactos"] == [{"tipo": "whatsapp", "valor": "523331221190"}]


def test_migrate_roundtrip_to_json(tmp_path):
    out = tmp_path / "estaciones.json"
    data = migrate(MD_SAMPLE)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    reloaded = json.loads(out.read_text(encoding="utf-8"))
    assert reloaded == data
