# SIGII Backend (FastAPI)

## Descripción general

Backend de SIGII construido con FastAPI, SQLAlchemy y Pydantic. Proporciona:
- Autenticación y autorización vía JWT.
- Gestión de inventario, solicitudes y flujo de estados.
- Conexión a dos bases de datos (principal y de usuarios).
- Documentación interactiva con OpenAPI.

## Routers

Cada router agrupa funcionalidades específicas:

- **/user**: extrae de los JWT las empresas, roles y organizaciones asociadas al usuario.
- **/producto**: consulta los registros de inventario (`tblInventarios_bck`) con filtros por bodega, empresa y categoría.
- **/organizacion**: lista los códigos de organización y asigna organizaciones a usuarios (`tblUsuarioOrganizacion`).
- **/tecnico**: crea peticiones de productos (`tblPeticiones_bck` + `tblProductosPeticion_bck`) y controla estados iniciales.
- **/bodega**: procesa productos pendientes, cambia su estado a "Procesando", "Listo para Entregar" y "Entregado", sincronizando la petición madre.

## Schemas

Modelos Pydantic en `app/schemas` para validar y serializar datos:

- Esquemas de lectura (`*Read`): definen la forma de respuestas JSON.
- Esquemas de creación/edición: validan los bodies de POST/PUT (e.j. `ProductoPeticionProcesando`, `UsuarioOrganizacionCreate`).

## Base de datos

- **app/database.py**: configura `engine` y `SessionLocal` para la base de datos principal (inventario y peticiones).
- **app/database2.py**: configura una segunda conexión (`get_db2`) para la base de datos de usuarios (`tblUsuario`) usando variables de entorno `DB2_*`.

## app/main.py

- Instancia la aplicación FastAPI.
- Aplica dependencias globales (`decode_jwt`, `require_app`).
- Incluye todos los routers.
- Configura CORS si es necesario.

## app/utils.py

Contiene funciones auxiliares:
- `decode_jwt`: dependencia para validar y decodificar tokens JWT usando clave pública.
- `require_role`, `require_app`: verifican roles y acceso a la aplicación dentro del payload JWT.

## app/settings.py

Lee variables de entorno desde `.env` usando `BaseSettings`:
- Parámetros de conexión a la base de datos principal.
- Mantiene `extra = ignore` para variables adicionales.

## Carpeta `certs`

Debe contener la clave pública PEM usada por JWT:
```
certs/jwt_private.pem.pub
```

## Estructura del archivo `.env`

```dotenv
# Base de datos principal
db_server=
db_port=
db_name=
db_user=
db_password=
driver=ODBC Driver 18 for SQL Server

# Base de datos secundaria (usuarios)
DB2_USER=
DB2_PASSWORD=
DB2_SERVER=
DB2_PORT=
DB2_NAME=
DB2_DRIVER=ODBC Driver 18 for SQL Server

# Servicio de productos (JWT)
PUBLIC_KEY_PATH=C:\Users\user\Desktop\SIGII-Backend-Fastapi\certs\jwt_private.pem.pub
ALGORITHM=RS256
```

## Prerrequisitos

- Python 3.10+
- SQL Server ODBC Driver 18
- Acceso a las bases de datos SQL Server

## Instalación

```bash
git clone https://.../SIGII-Backend-Fastapi.git
cd SIGII-Backend-Fastapi
python -m venv .venv
. .venv/Scripts/activate        # Windows PowerShell
pip install -r requirements.txt
```

## Configuración

Crear fichero `.env` en la raíz con variables:

# Base de datos principal
DB_USER=<usuario>
DB_PASSWORD=<clave>
DB_SERVER=<host o IP>
DB_PORT=<puerto>
DB_NAME=<nombre_bd>
DRIVER={ODBC Driver 18 for SQL Server}

# Base de datos de autenticación (tblUsuario)
DB2_USER=<usuario2>
DB2_PASSWORD=<clave2>
DB2_SERVER=<host2>
DB2_PORT=<puerto2>
DB2_NAME=<nombre_bd2>
DB2_DRIVER={ODBC Driver 18 for SQL Server}

# JWT (utils)
PUBLIC_KEY_PATH=<ruta_al_pem.pub>
ALGORITHM=RS256

## Ejecución

```bash
uvicorn app.main:app --reload
```

Se expondrán los endpoints en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

## Endpoints principales

### Autenticación
*(externa)*
- `POST /token`: obtener JWT.

### Usuario
- `GET /user/empresa` → Lista de empresas.
- `GET /user/rol` → Lista de roles.
- `GET /user/organizacion` → Lista de códigos de organización.

### Inventario
- `GET /producto` → Listado de inventario filtrable con query params: `bodega`, `empresa`, `categoria`.

### Organizaciones (Asignar bodegas)
- `GET /organizacion/codigos` → Todos los códigos de organización.
- `POST /organizacion/agregar` → Asigna `{ correo, codigo }` en tblUsuarioOrganizacion.

### Técnico (Solicitudes)
- `POST /tecnico/solicitud` → Crea una solicitud (`tblPeticiones_bck` + `tblProductosPeticion_bck`).

### Bodega (Procesamiento)
- `GET /bodega/pendientes` → Productos pendientes.
- `GET /bodega/pendientes/peticiones` → Peticiones con productos pendientes (únicas).
- `POST /bodega/pendientes/procesando` → Marca producto como `Procesando`.
- `POST /bodega/pendientes/listoParaEntregar` → Marca producto como `Listo para Entregar`.
- `POST /bodega/pendientes/entregado` → Marca producto como `Entregado`.

## Modelos (Schemas)

- **EmpresaRead**: `{ nombre: str }`
- **RolRead**: `{ nombre: str }`
- **OrganizacionRead**: `{ nombre: str }`
- **CodigoOrganizacion**: `{ codigo: str }`
- **UsuarioOrganizacionCreate**: `{ correo: str, codigo: str }`
- **InventarioRead**: campos básicos de inventario.
- **ProductoPeticionRead**: DTO de `tblProductosPeticion_bck`.
- **ProductoPeticionProcesando**: `{ idPeticionProducto: int, comentario?: str }`
- **ProductoPeticionProcesado**: `{ idPeticionProducto: int, comentario?: str, solicitadaEntregada?: int, cantidadProcesada?: float }`
- **ProductoPeticionEntregado**: `{ idPeticionProducto: int, comentario?: str, entregadoA: str }`
- **PeticionRead**: DTO de `tblPeticiones_bck`.

## Contribuir

1. Fork del repositorio.
2. Crear feature branch.
3. Hacer commit con buenas descripciones.
4. Abrir PR.

## Licencia

Sin licencia especificada. Solicitar al equipo de arquitectos.
