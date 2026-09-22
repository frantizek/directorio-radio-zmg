# Directorio de Radio ZMG

Directorio web de las principales estaciones de radio FM y AM de la Zona Metropolitana de Guadalajara (ZMG), México. Incluye frecuencia, nombre, contactos (teléfono, WhatsApp, redes sociales, web, email), programas con horario y locutores, y estado de verificación.

## Sitio web

El directorio está publicado en GitHub Pages: **https://frantizek.github.io/directorio-radio-zmg/**

Para desplegarlo en otro repositorio:

1. Crea un repositorio en GitHub y sube este código.
2. En **Settings → Pages → Source**, selecciona *Deploy from a branch* → `main` → `/` (root).
3. Edita `js/config.js` y pon tu usuario de GitHub en `CONFIG.owner`.
4. Crea un *fine-grained personal access token* con permisos **Contents: read/write** y **Pull requests: read/write** sobre el repositorio.
5. En la web, usa el botón **Iniciar sesión** para pegar el token.

## Cómo editar los datos

- La **fuente de verdad** es `data/estaciones.json`.
- Desde la web (con sesión iniciada) puedes añadir, editar o eliminar estaciones, contactos y programas. Al guardar, la aplicación crea una rama, commitea el JSON y abre un **pull request** para revisar los cambios.
- También puedes editar el JSON directamente y regenerar el README con el script.

## Estructura del proyecto

- `data/estaciones.json` — datos estructurados (estaciones, contactos, programas).
- `index.html`, `css/`, `js/` — frontend estático (Alpine.js, i18n es/en, cliente de la API de GitHub).
- `scripts/migrate.py` — migración única de las tablas del README al JSON.
- `scripts/generate_readme.py` — regenera las tablas del README desde el JSON.
- `tests/` — pruebas de pytest.

## Desarrollo

```bash
uv run python scripts/migrate.py        # README -> data/estaciones.json
uv run python scripts/generate_readme.py # data/estaciones.json -> README
uv run pytest                            # ejecutar tests
uv run ruff check .                      # linter
python -m http.server 8000               # servir la web localmente
```

**Nota:** Los números pueden cambiar. Se recomienda verificar en los sitios web oficiales para la información más reciente.

---

## Estaciones de FM (Frecuencia Modulada)

<!-- TABLA_FM -->
| Frecuencia | Nombre de la Estación y Programas | ☎️ Teléfono Fijo | Número de WhatsApp | Verificado |
| :--- |:------------------------------------------------| :--- |:---------------------------------------------------------|:-----------|
| 88.7 MHz | **ArrobaFM** | 3338250887 | `No disponible` | ✅ |
| 89.1 MHz | **RMX** |  | `No disponible` |  |
| 89.9 MHz | **Magia Digital** |  | [33 1972 7663](http://wa.me/523319727663) | ✅ |
| 90.3 MHz | **Match FM** |  | [33 1188 5013](http://wa.me/523311885013) |  |
| 90.7 MHz | **Señal 90** |  | [33 3813 1313](http://wa.me/523338131313) |  |
| 91.5 MHz | **Zona Tres** |  | [33 1880 7641](http://wa.me/523318807641) | ✅ |
| 91.9 MHz | **Rock & Soul** |  | [33 1409 9399](http://wa.me/523314099399) | ✅ |
| 92.3 MHz | **Fiesta Mexicana** |  | [33 3121 9230](http://wa.me/523331219230) |  |
| 92.7 MHz | **Radio Mujer** |  | `No disponible` |  |
| 93.1 MHz | **Amor 93.1** |  | [33 1019 7931](http://wa.me/523310197931) |  |
| 93.9 MHz | **Imagen Radio Guadalajara** |  | [55 1951 6846](http://wa.me/525519516846) |  |
| 94.7 MHz | **KY 94.7** |  | [33 2823 3699](http://wa.me/523328233699) | ✅ |
| 95.5 MHz | **La Mejor** |  | [33 1974 7955](http://wa.me/523319747955) |  |
| 95.9 MHz | **Vox Radio Hits** |  | [33 1974 7955](http://wa.me/523319747955) |  |
| 96.3 MHz | **Jalisco Radio** |  | `No disponible` |  |
| 97.1 MHz | **La Ke Buena** |  | [33 3812 0971](http://wa.me/523338120971) |  |
| 97.9 MHz | **Fórmula Melódica** |  | [33 3812 0971](http://wa.me/523338120971) |  |
| 98.7 MHz | **Globo** |  | `No disponible` |  |
| 99.5 MHz | **Romance** |  | [33 1409 9408](http://wa.me/523314099408) | ✅ |
| 99.9 MHz | **Exa FM** |  | [33 1019 7999](http://wa.me/523310197999) |  |
| 100.3 MHz | **Heraldo Radio** |  | [33 3122 1190](http://wa.me/523331221190) |  |
| 101.1 MHz | **Exa FM 101.1** |  | [33 3813 1313](http://wa.me/523338131313) |  |
| 101.9 MHz | **La Buena Onda** |  | [33 3813 1313](http://wa.me/523338131313) |  |
| 102.7 MHz | **Los 40** |  | [33 3647 1027](http://wa.me/523336471027) |  |
| 103.5 MHz | **La Tapatia** |  | [33 3647 1027](http://wa.me/523336471027) |  |
| 104.3 MHz | **Radio UdeG** <br/> ▸ *El Expreso de las Diez* | 3317160006 | **General:** [33 2053 6975](http://wa.me/523320536975) ✅ | ✅ |
| 105.1 MHz | **Milenio Bella Musica** |  | `No disponible` |  |
| 105.9 MHz | **Éxtasis Digital** |  | [33 1404 0979](http://wa.me/523314040979) |  |
| 106.7 MHz | **Máxima FM** |  | [33 1199 0735](http://wa.me/523311990735) |  |
| 107.5 MHz | **Retro 107.5** |  | [33 3467 7220](http://wa.me/523334677220) | ✅ |
<!-- /TABLA_FM -->

---

## Estaciones de AM (Amplitud Modulada)

<!-- TABLA_AM -->
| Frecuencia | Nombre de la Estación | ☎️ Teléfono Fijo | Número de WhatsApp | Verificado |
| :--- |:------------------------------------------------| :--- |:---------------------------------------------------------|:-----------|
| 580 kHz | **Radio 580** |  | [33 3122 1190](http://wa.me/523331221190) |  |
| 630 kHz | **Jalisco Radio** |  | [33 3678 0094](http://wa.me/523336780094) |  |
| 710 kHz | **Radio María** |  | [33 2301 2294](http://wa.me/523323012294) |  |
| 760 kHz | **Radio Cañón** |  | `No disponible` |  |
| 790 kHz | **W Radio** |  | [55 1381 2222](http://wa.me/525513812222) |  |
| 850 kHz | **Notisistema** |  | [33 1880 8692](http://wa.me/523318808692) |  |
| 920 kHz | **La Voz de la FE** |  | `No disponible` |  |
| 1010 kHz | **Radio Ranchito** |  | [33 3812 3790](http://wa.me/523338123790) |  |
| 1070 kHz | **Radio Vital** |  | [33 3813 1313](http://wa.me/523338131313) |  |
| 1110 kHz | **Radio Comerciales** |  | `No disponible` |  |
| 1150 kHz | **Radio Metrópoli** |  | [33 1155 1962](http://wa.me/523311551962) | ✅ |
| 1190 kHz | **W Radio Guadalajara** |  | `No disponible` |  |
| 1250 kHz | **DK 1250** | 3336477481 | [33 2944 9080](http://wa.me/523329449080) | ✅ |
| 1310 kHz | **Radio Vital** |  | [33 3813 1313](http://wa.me/523338131313) |  |
| 1340 kHz | **Frecuencia Deportiva** |  | [33 3122 5933](http://wa.me/523331225933) |  |
| 1410 kHz | **Campirana** |  | [33 3812 2510](http://wa.me/523338122510) |  |
| 1480 kHz | **Ondas de la Alegría** |  | [33 3678 0094](http://wa.me/523336780094) |  |
<!-- /TABLA_AM -->
