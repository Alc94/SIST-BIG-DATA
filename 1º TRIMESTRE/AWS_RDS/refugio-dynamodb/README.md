# Refugio de perros: DynamoDB con Boto3

Parte de DynamoDB del proyecto del refugio (las tablas "fijas" están en RDS, en `refugio-perros`).

## Tablas
| Tabla | Clave de partición | Clave de ordenación | Índices |
|---|---|---|---|
| `historial_medico` | `perro_id` (N) | `fecha` (S) | Local `TipoIndex` (perro_id + tipo) |
| `registro_paseos` | `perro_id` (N) | `fecha_hora` (S) | – |
| `solicitudes_adopcion` | `adoptante_id` (N) | `fecha_solicitud` (S) | Global `EstadoFechaIndex` (estado + fecha_solicitud) |

`perro_id` y `adoptante_id` son los `id` de las tablas `perros` y `adoptantes` de RDS.

## Archivos (uno por operación)
- `conectarse.py`: sesión de Boto3 (client y resource) con las claves del `.env`.
- `crearTablaHistorialMedico.py`, `crearTablaRegistroPaseos.py`, `crearTablaSolicitudesAdopcion.py`: crean las tablas.
- `crearIndiceGlobal.py`: añade el índice global a `solicitudes_adopcion`.
- `crearElementos.py`, `crearElementosJSON.py`: insertan datos de ejemplo (`put_item`).
- `mostrarElementos.py`: `scan` con filtro. `obtenerUnElemento.py`: `get_item`.
- `eliminarTabla.py`: borra una tabla.
- `main_dynamodb.py`: ejecuta todo explicando cada función y su resultado en JSON.

## Uso
```
python -m venv venv-refugio
source venv-refugio/Scripts/activate      # Git Bash en Windows
pip install -r requirements.txt
cp .env.example .env                       # y pega las claves del laboratorio
python probar_dynamodb.py
python main_dynamodb.py
```
