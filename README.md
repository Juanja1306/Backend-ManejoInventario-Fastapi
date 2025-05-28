# SIGII Backend (FastAPI)

API backend para el sistema SIGII, construido con FastAPI y SQLAlchemy.

## Características

- Autenticación y autorización por JWT (RS256).
- Múltiples routers:
  - **/user**: obtiene empresas, roles y organizaciones de un usuario a partir del JWT.
  - **/producto**: consulta inventario con filtros por bodega, empresa y categoría.
  - **/organizacion**: lista y asigna bodegas a usuarios.
  - **/tecnico**: crea solicitudes de productos y gestiona estados (Procesando, Listo para Entregar, Entregado).
  - **/bodega**: consume solicitudes pendientes y gestiona su flujo.
- Conexión a dos bases de datos: principal y de autenticación de usuarios.
- Validaciones de flujo de estados y consistencia de datos.
- Documentación OpenAPI en `/docs`.

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
