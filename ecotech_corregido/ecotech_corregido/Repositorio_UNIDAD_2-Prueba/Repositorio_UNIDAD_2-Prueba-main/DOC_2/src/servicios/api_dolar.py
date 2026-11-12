"""Consumo de la API de indicadores económicos (mindicador.cl) — paso 3.1.1."""
import math
import os

from servicios.http_cliente import obtener_json

URL_DOLAR = os.getenv("API_DOLAR_URL", "https://mindicador.cl/api/dolar")


def obtener_datos():
    """Pide los datos del dólar y devuelve el JSON ya convertido a dict."""
    return obtener_json(URL_DOLAR)


def extraer_primero(datos):
    """Valida la serie y devuelve (fecha, valor) del primer registro.

    El valor debe ser numérico, finito y mayor que cero.
    """
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada: se esperaba un diccionario.")

    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles en la serie.")

    registro = serie[0]
    if not isinstance(registro, dict):
        raise ValueError("El formato del registro es inválido.")
    if "valor" not in registro or "fecha" not in registro:
        raise ValueError("El registro no contiene las claves 'valor' o 'fecha'.")

    valor, fecha = registro["valor"], registro["fecha"]
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        raise ValueError("El valor del indicador debe ser numérico.")
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError("El valor del indicador debe ser finito y mayor que cero.")
    return fecha, valor
