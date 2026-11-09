from dominio.permisos import exigir_sesion


def consultar_indicador(sesion):
    exigir_sesion(sesion)
    return None


def obtener_historial(sesion):
    exigir_sesion(sesion)
    return []