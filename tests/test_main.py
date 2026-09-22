import json

import pandas as pd

import main

MD_TWO_TABLES = """# Encabezado

## Tabla FM

| Frecuencia | Nombre de la Estación | ☎️ Teléfono Fijo | Verificado |
| :--- | :--- | :--- | :--- |
| 88.7 MHz | **ArrobaFM** | 3338250887 | ✅ |

## Tabla AM

| Frecuencia | Nombre de la Estación | ☎️ Teléfono Fijo | Verificado |
| :--- | :--- | :--- | :--- |
| 580 kHz | **Radio 580** | | |
"""


def test_clean_column_names_lowercases_and_removes_symbols():
    df = pd.DataFrame(
        {"Nombre de la Estación y Programas": ["X"], "☎️ Teléfono Fijo": ["1"]}
    )
    df = main.clean_column_names(df)
    assert list(df.columns) == ["nombre_de_la_estación_y_programas", "teléfono_fijo"]


def test_markdown_to_json_creates_fm_and_am_lists(tmp_path):
    in_file = tmp_path / "radio.md"
    out_file = tmp_path / "radio.json"
    in_file.write_text(MD_TWO_TABLES, encoding="utf-8")

    main.markdown_to_json(str(in_file), str(out_file))

    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert set(data.keys()) == {"estaciones_fm", "estaciones_am"}
    assert len(data["estaciones_fm"]) == 1
    assert len(data["estaciones_am"]) == 1

    fm = data["estaciones_fm"][0]
    assert fm["frecuencia"] == "88.7 MHz"
    assert fm["nombre_de_la_estación"] == "ArrobaFM"
    assert fm["verificado"] == "✅"

    am = data["estaciones_am"][0]
    assert am["frecuencia"] == "580 kHz"
    assert am["nombre_de_la_estación"] == "Radio 580"
    assert am["teléfono_fijo"] is None


def test_markdown_to_json_returns_none_for_missing_file(tmp_path, capsys):
    missing = tmp_path / "no-existe.md"
    assert main.markdown_to_json(str(missing), str(tmp_path / "out.json")) is None
    assert "no fue encontrado" in capsys.readouterr().out


def test_markdown_to_json_returns_none_without_two_tables(tmp_path):
    in_file = tmp_path / "una.md"
    out_file = tmp_path / "out.json"
    in_file.write_text("| A | B |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
    assert main.markdown_to_json(str(in_file), str(out_file)) is None
    assert not out_file.exists()
