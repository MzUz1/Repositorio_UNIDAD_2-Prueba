"""Cliente HTTP común para las APIs externas (pasos 3.1.1 y 3.1.3)."""
import os

import requests
from requests.exceptions import ConnectionError as ErrorConexionHTTP
from requests.exceptions import RequestException, Timeout

from registro_errores import log

TIMEOUT = (
    float(os.getenv("API_TIMEOUT_CONEXION", "3")),
    float(os.getenv("API_TIMEOUT_LECTURA", "5")),
)


class ErrorServicioExterno(Exception):
    """El mensaje de esta excepción es seguro para mostrarse al usuario."""


def obtener_json(url, params=None, llave=None):
    """GET que devuelve el JSON ya procesado o lanza ErrorServicioExterno.

    - Controla timeout y fallas de conexión.
    - Valida el código HTTP (200, 404, 401/403, 429, 5xx y otros).
    - 'llave' (opcional) viaja solo en un encabezado; nunca se escribe en
      el log ni en pantalla.
    """
    headers = {"Authorization": f"Bearer {llave}"} if llave else None
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
    except Timeout:
        log.error("Timeout al consultar %s", url)
        raise ErrorServicioExterno("El servicio tardó demasiado en responder.")
    except ErrorConexionHTTP:
        log.error("Sin conexión con %s", url)
        raise ErrorServicioExterno("No hay conexión con el servicio externo.")
    except RequestException as e:
        log.error("Error de requests en %s: %s", url, type(e).__name__)
        raise ErrorServicioExterno("No se pudo consultar el servicio externo.")

    codigo = resp.status_code
    if codigo == 200:
        try:
            return resp.json()
        except ValueError:
            log.error("JSON inválido desde %s", url)
            raise ErrorServicioExterno("El servicio devolvió una respuesta no válida.")

    log.error("HTTP %s desde %s", codigo, url)
    if codigo == 404:
        raise ErrorServicioExterno("No se encontró la información solicitada.")
    if codigo in (401, 403):
        raise ErrorServicioExterno("El servicio rechazó el acceso. Revise la configuración.")
    if codigo == 429:
        raise ErrorServicioExterno("Demasiadas consultas al servicio. Espere un momento.")
    if codigo >= 500:
        raise ErrorServicioExterno("El servicio externo tiene problemas. Intente más tarde.")
    raise ErrorServicioExterno(f"Respuesta inesperada del servicio ({codigo}).")
