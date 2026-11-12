# EcoTech – cambios para cumplir 3.1.1, 3.1.2 y 3.1.3

Copia el contenido de este zip sobre tu repositorio (misma estructura de carpetas).
Y **borra a mano** `DOC_2/src/persistencia/usuariio.py` (fragmento huérfano con error de sintaxis).

## Pasos para probar
1. `pip install -r requirements.txt`   (ahora incluye `requests` y `bcrypt`)
2. `python crear_admin.py`   (desde `DOC_2/src`; crea el 1.er empleado + usuario admin)
3. `python main.py`

## Bugs corregidos en tu código
| Archivo | Problema | Arreglo |
|---|---|---|
| `servicios/autenticacion.py` | La sesión no traía `rol`, pero `exigir_sesion` lo exige: todo daba "Acceso no permitido" | Devuelve `rol`; el DAO lo lee de la BD |
| `persistencia/crear_db.py` | No creaba `usuario` ni `indicador_api` | Se agregan ambas tablas (y al .sql) |
| `dominio/deserializador_indicador.py` | Importaba `servicios.api_dolar`, que no existía | Se crea `servicios/api_dolar.py` con tu `extraer_primero` |
| `persistencia/indicador_dao.py` | Sintaxis SQLite (`?`, `ON CONFLICT`) en un proyecto MySQL | Reescrito con `%s` y `ON DUPLICATE KEY UPDATE` |
| `ux/interfaz.py` | `print(f"Error: {e}")` mostraba errores internos | Excepciones separadas + `errores.log` |
| `persistencia/conexion.py` | El mensaje incluía el error de MySQL (host/usuario) | Mensaje genérico; el detalle va al log |
| `persistencia/usuario_dao.py` | SQL armado con f-string (`{columna}`) | Lista blanca de columnas |
| `servicios/autenticacion.py` | Imprimía "No se encontró la cuenta…" (revela qué usuarios existen) | Mensaje único + hash de relleno |
| `dominio/menu_usuario.py` | `consultar_indicador` y `menu_privado` eran stubs sin uso | Eliminados; el menú real está en `interfaz.py` |

## Qué cubre cada paso
- **3.1.1 APIs**: `servicios/api_dolar.py` (mindicador.cl), `servicios/clima.py` (Open-Meteo), `servicios/indicadores.py` (historial en MySQL y pago en USD). Menú 11–14.
- **3.1.2 Seguridad**: login obligatorio (3 intentos) en `main.py`, bcrypt, `dominio/validadores.py`, acciones solo-admin (eliminar empleado, pago en USD, crear cuentas), configuración en `.env`.
- **3.1.3 Errores**: `servicios/http_cliente.py` (timeout, conexión, 200/404/401/403/429/5xx), `registro_errores.py` → `errores.log` (ya en `.gitignore`).

## Archivos nuevos
`registro_errores.py`, `crear_admin.py`, `servicios/http_cliente.py`, `servicios/api_dolar.py`, `servicios/clima.py`, `dominio/validadores.py`

## Nota
`main_prueba.py` (raíz y `src/`) quedó igual; su lógica ya vive en `servicios/api_dolar.py`, puedes borrarlos.
