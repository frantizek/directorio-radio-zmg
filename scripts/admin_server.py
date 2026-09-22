"""Servidor web local de administración del directorio.

Levanta un servidor HTTP en `127.0.0.1:8001` que sirve la interfaz de
administración (`admin/`) y una API REST para hacer CRUD sobre
`data/estaciones.json`. Cada escritura normaliza los datos, guarda el JSON y
regenera el README.

Uso:
    uv run python scripts/admin_server.py
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.estaciones import (
    DATA_PATH,
    README_PATH,
    find_duplicate,
    load_estaciones,
    normalize_estacion,
    save_estaciones,
)

ADMIN_DIR = ROOT / "admin"

HOST = "127.0.0.1"
PORT = 8001


class Store:
    """Acceso a los datos: carga y guarda el JSON regenerando el README."""

    def __init__(self, data_path=DATA_PATH, readme_path=README_PATH):
        self.data_path = data_path
        self.readme_path = readme_path

    def load(self):
        return load_estaciones(self.data_path)

    def save(self, estaciones):
        save_estaciones(estaciones, self.data_path, self.readme_path)


def create_estacion(estaciones, payload):
    """Crea una estación. Devuelve (status, body, nueva_lista)."""
    estacion = normalize_estacion(payload)
    if not estacion:
        return 400, {"error": "incomplete"}, None
    nueva = estaciones + [estacion]
    if find_duplicate(nueva):
        return 400, {"error": "duplicate"}, None
    return 201, estacion, nueva


def update_estacion(estaciones, estacion_id, payload):
    """Actualiza una estación. Devuelve (status, body, nueva_lista)."""
    if not any(e["id"] == estacion_id for e in estaciones):
        return 404, {"error": "not_found"}, None
    estacion = normalize_estacion(payload)
    if not estacion:
        return 400, {"error": "incomplete"}, None
    nueva = [estacion if e["id"] == estacion_id else e for e in estaciones]
    if find_duplicate(nueva):
        return 400, {"error": "duplicate"}, None
    return 200, estacion, nueva


def delete_estacion(estaciones, estacion_id):
    """Elimina una estación. Devuelve (status, body, nueva_lista)."""
    if not any(e["id"] == estacion_id for e in estaciones):
        return 404, {"error": "not_found"}, None
    nueva = [e for e in estaciones if e["id"] != estacion_id]
    return 204, None, nueva


class AdminHandler(BaseHTTPRequestHandler):
    store = None

    def log_message(self, fmt, *args):
        print(f"[admin] {self.address_string()} - {fmt % args}")

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, content_type):
        try:
            body = path.read_bytes()
        except OSError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _apply(self, operation, estacion_id=None):
        payload = self._read_json() if self.command in ("POST", "PUT") else None
        estaciones = self.store.load()
        if operation == "create":
            status, body, nueva = create_estacion(estaciones, payload)
        elif operation == "update":
            status, body, nueva = update_estacion(estaciones, estacion_id, payload)
        else:
            status, body, nueva = delete_estacion(estaciones, estacion_id)
        if status < 300:
            self.store.save(nueva)
        self._send_json(status, body if body is not None else {})

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_file(ADMIN_DIR / "index.html", "text/html; charset=utf-8")
        elif self.path == "/admin.js":
            self._send_file(ADMIN_DIR / "admin.js", "application/javascript; charset=utf-8")
        elif self.path == "/admin.css":
            self._send_file(ADMIN_DIR / "admin.css", "text/css; charset=utf-8")
        elif self.path == "/css/style.css":
            self._send_file(ROOT / "css" / "style.css", "text/css; charset=utf-8")
        elif self.path == "/api/estaciones":
            self._send_json(200, {"estaciones": self.store.load()})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/estaciones":
            self.send_error(404)
            return
        self._apply("create")

    def do_PUT(self):
        match = re.fullmatch(r"/api/estaciones/([^/]+)", self.path)
        if not match:
            self.send_error(404)
            return
        self._apply("update", unquote(match.group(1)))

    def do_DELETE(self):
        match = re.fullmatch(r"/api/estaciones/([^/]+)", self.path)
        if not match:
            self.send_error(404)
            return
        self._apply("delete", unquote(match.group(1)))


def main():
    AdminHandler.store = Store()
    server = ThreadingHTTPServer((HOST, PORT), AdminHandler)
    print(f"Admin del directorio en http://{HOST}:{PORT}")
    print("Presiona Ctrl+C para detener.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()