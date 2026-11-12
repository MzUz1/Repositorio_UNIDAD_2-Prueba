"""Consumo de API de clima (Open-Meteo, sin llave) — paso 3.1.1."""
import os
import unicodedata

from dominio.permisos import exigir_sesion
from dominio.validadores import validar_ciudad, validar_pais
from servicios.http_cliente import ErrorServicioExterno, obtener_json

URL_GEOCODING = os.getenv("API_GEOCODING_URL", "https://geocoding-api.open-meteo.com/v1/search")
URL_CLIMA = os.getenv("API_CLIMA_URL", "https://api.open-meteo.com/v1/forecast")

_ESTADOS = {
    0: "despejado", 1: "mayormente despejado", 2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 48: "niebla", 51: "llovizna", 53: "llovizna", 55: "llovizna",
    61: "lluvia", 63: "lluvia", 65: "lluvia fuerte", 71: "nieve", 73: "nieve",
    75: "nieve fuerte", 80: "chubascos", 81: "chubascos", 82: "chubascos fuertes",
    95: "tormenta eléctrica", 96: "tormenta con granizo", 99: "tormenta con granizo",
}
# Condiciones que ponen en riesgo las actividades al aire libre de un proyecto
_RIESGO = {45, 48, 61, 63, 65, 71, 73, 75, 80, 81, 82, 95, 96, 99}
_VIENTO_RIESGO_KMH = 40


def _normalizar(texto):
    sin_tildes = unicodedata.normalize("NFD", texto)
    return "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn").lower()


def consultar_clima(sesion, ciudad, pais):
    """Clima actual de una ciudad, con alerta para la planificación de proyectos."""
    exigir_sesion(sesion)
    ciudad = validar_ciudad(ciudad)
    pais = validar_pais(pais)

    geo = obtener_json(URL_GEOCODING, {"name": ciudad, "count": 10, "language": "es"})
    if not isinstance(geo, dict):
        raise ErrorServicioExterno("El servicio devolvió una respuesta no válida.")
    buscado = _normalizar(pais)
    lugares = [r for r in (geo.get("results") or [])
               if buscado in _normalizar(r.get("country") or "")]
    if not lugares:
        raise ErrorServicioExterno(f"No se encontró '{ciudad}' en '{pais}'.")
    lugar = lugares[0]

    datos = obtener_json(URL_CLIMA, {
        "latitude": lugar["latitude"], "longitude": lugar["longitude"],
        "current": "temperature_2m,weather_code,wind_speed_10m", "timezone": "auto",
    })
    actual = datos.get("current") if isinstance(datos, dict) else None
    temperatura = actual.get("temperature_2m") if actual else None
    if not isinstance(temperatura, (int, float)):
        raise ErrorServicioExterno("El servicio no entregó datos de clima utilizables.")

    codigo = actual.get("weather_code", -1)
    viento = actual.get("wind_speed_10m") or 0
    riesgo = codigo in _RIESGO or viento >= _VIENTO_RIESGO_KMH
    return {
        "ciudad": lugar.get("name", ciudad),
        "pais": lugar.get("country", pais),
        "temperatura_c": temperatura,
        "estado": _ESTADOS.get(codigo, "sin descripción"),
        "viento_kmh": viento,
        "riesgo_operativo": riesgo,
        "recomendacion": ("Considere reprogramar las actividades al aire libre."
                          if riesgo else "Condiciones adecuadas para operar."),
    }
