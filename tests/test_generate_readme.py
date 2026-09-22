from scripts.generate_readme import (
    format_frecuencia,
    format_nombre,
    format_telefono,
    format_whatsapp,
    generate,
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


def test_generate_creates_two_tables():
    md = generate(DATA_SAMPLE)
    assert "## Estaciones de FM (Frecuencia Modulada)" in md
    assert "## Estaciones de AM (Amplitud Modulada)" in md
    assert "**ArrobaFM**" in md
    assert "**Radio UdeG** <br/> ▸ *El Expreso de las Diez*" in md
    assert "**General:** [33 2053 6975](http://wa.me/523320536975) ✅" in md
    assert "**Radio 580**" in md
