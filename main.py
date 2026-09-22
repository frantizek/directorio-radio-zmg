import io
import json
import re

import markdown
import pandas as pd


def clean_column_names(df):
    """
    Limpia y estandariza los nombres de las columnas del DataFrame.
    Convierte a minúsculas, reemplaza espacios con guiones bajos y elimina emojis.
    """
    cleaned_columns = []
    for col in df.columns:
        # Convierte a minúsculas y quita espacios en los bordes
        cleaned_col = col.lower().strip()
        # Elimina emojis y símbolos que no sean espacios, letras o números
        cleaned_col = re.sub(r"[^\w\s]", "", cleaned_col)
        # Reemplaza espacios por guion bajo
        cleaned_col = re.sub(r"\s+", "_", cleaned_col).strip("_")
        cleaned_columns.append(cleaned_col)
    df.columns = cleaned_columns
    return df


def markdown_to_json(markdown_file_path, json_file_path):
    """
    Lee un archivo Markdown con tablas de radio, lo procesa y lo guarda como JSON.
    """
    print(f"Iniciando la conversión de '{markdown_file_path}'...")

    # 1. Leer el archivo Markdown
    try:
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{markdown_file_path}' no fue encontrado.")
        return

    # 2. Convertir el contenido Markdown a HTML
    # La extensión 'tables' es necesaria para que la librería reconozca las tablas.
    html = markdown.markdown(md_content, extensions=["markdown.extensions.tables"])

    # 3. Usar pandas para leer las tablas del HTML generado
    try:
        tables = pd.read_html(io.StringIO(html))
        if len(tables) < 2:
            print(
                "Error: No se encontraron las dos tablas esperadas (FM y AM) en el archivo."
            )
            return
        df_fm = tables[0]
        df_am = tables[1]
    except ValueError:
        print(
            "Error: Pandas no pudo encontrar ninguna tabla en el contenido del archivo."
        )
        return

    # 4. Limpiar los DataFrames
    df_fm = clean_column_names(df_fm)
    df_am = clean_column_names(df_am)

    # Reemplazar los valores NaN (Not a Number) de pandas por None para un JSON limpio
    df_fm = df_fm.astype(object).where(pd.notna(df_fm), None)
    df_am = df_am.astype(object).where(pd.notna(df_am), None)

    # 5. Convertir los DataFrames a una lista de diccionarios (formato ideal para JSON)
    fm_list = df_fm.to_dict("records")
    am_list = df_am.to_dict("records")

    # 6. Crear la estructura final del JSON
    final_data = {"estaciones_fm": fm_list, "estaciones_am": am_list}

    # 7. Escribir el diccionario en un archivo JSON
    with open(json_file_path, "w", encoding="utf-8") as f:
        # ensure_ascii=False para guardar correctamente acentos y emojis.
        # indent=4 para que el archivo sea legible para humanos.
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    print(f"¡Éxito! Los datos han sido guardados en '{json_file_path}'.")


# --- Ejecución del script ---
if __name__ == "__main__":
    # Define los nombres de los archivos de entrada y salida
    input_md_file = "README.md"
    output_json_file = "radio_guadalajara.json"

    markdown_to_json(input_md_file, output_json_file)
