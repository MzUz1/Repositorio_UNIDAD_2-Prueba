"""Registro de errores en archivo (paso 3.1.3).

El detalle técnico se guarda en errores.log; al usuario solo se le
muestran mensajes genéricos, sin hosts, usuarios, rutas ni llaves.
"""
import logging

logging.basicConfig(
    filename="errores.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)
log = logging.getLogger("ecotech")
