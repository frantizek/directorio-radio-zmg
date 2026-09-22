from scripts.admin_server import create_estacion, delete_estacion, update_estacion

BASE = [
    {
        "id": "fm-88.7",
        "banda": "FM",
        "frecuencia": "88.7",
        "nombre": "ArrobaFM",
        "verificado": True,
        "contactos": [],
        "programas": [],
    }
]

PAYLOAD = {
    "banda": "FM",
    "frecuencia": "104.3",
    "nombre": "Radio UdeG",
    "verificado": False,
    "contactos": [{"tipo": "whatsapp", "valor": "523320536975"}],
    "programas": [],
}


def test_create_estacion_ok():
    status, body, nueva = create_estacion(BASE, PAYLOAD)
    assert status == 201
    assert body["id"] == "fm-104.3"
    assert len(nueva) == 2


def test_create_estacion_duplicate():
    status, body, nueva = create_estacion(BASE, {"banda": "FM", "frecuencia": "88.7", "nombre": "Otra"})
    assert status == 400
    assert body == {"error": "duplicate"}
    assert nueva is None


def test_create_estacion_incomplete():
    status, body, nueva = create_estacion(BASE, {"banda": "FM", "frecuencia": "", "nombre": ""})
    assert status == 400
    assert body == {"error": "incomplete"}
    assert nueva is None


def test_update_estacion_ok():
    payload = dict(PAYLOAD, nombre="Radio UdeG Editada")
    status, body, nueva = update_estacion(BASE, "fm-88.7", payload)
    assert status == 200
    assert body["nombre"] == "Radio UdeG Editada"
    assert nueva[0]["id"] == "fm-104.3"


def test_update_estacion_not_found():
    status, body, nueva = update_estacion(BASE, "fm-999", PAYLOAD)
    assert status == 404
    assert body == {"error": "not_found"}
    assert nueva is None


def test_update_estacion_duplicate():
    base = BASE + [
        {
            "id": "fm-104.3",
            "banda": "FM",
            "frecuencia": "104.3",
            "nombre": "Radio UdeG",
            "verificado": False,
            "contactos": [],
            "programas": [],
        }
    ]
    status, body, nueva = update_estacion(
        base, "fm-88.7", {"banda": "FM", "frecuencia": "104.3", "nombre": "X"}
    )
    assert status == 400
    assert body == {"error": "duplicate"}
    assert nueva is None


def test_delete_estacion_ok():
    status, body, nueva = delete_estacion(BASE, "fm-88.7")
    assert status == 204
    assert body is None
    assert nueva == []


def test_delete_estacion_not_found():
    status, body, nueva = delete_estacion(BASE, "fm-999")
    assert status == 404
    assert body == {"error": "not_found"}
    assert nueva is None