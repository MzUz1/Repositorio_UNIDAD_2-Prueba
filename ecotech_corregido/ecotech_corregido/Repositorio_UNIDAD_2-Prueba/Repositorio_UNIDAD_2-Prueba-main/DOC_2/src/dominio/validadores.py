"""Validadores de entradas del usuario (paso 3.1.2).

Siguen el patrón de dominio/entradas.pedir_dato: reciben el texto y
devuelven el valor limpio, o lanzan ValueError con un mensaje seguro.
"""
import re

_TEXTO = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ .'\-]{1,59}")


def _texto(valor, etiqueta, valido):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{etiqueta} no puede estar vacío.")
    valor = " ".join(valor.split())
    if not _TEXTO.fullmatch(valor):
        raise ValueError(f"{etiqueta} no es {valido}: use solo letras (2 a 60 caracteres).")
    return valor


def validar_ciudad(valor):
    return _texto(valor, "La ciudad", "válida")


def validar_pais(valor):
    return _texto(valor, "El país", "válido")
