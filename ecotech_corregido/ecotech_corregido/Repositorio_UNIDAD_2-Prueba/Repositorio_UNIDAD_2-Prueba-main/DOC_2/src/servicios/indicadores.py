"""Indicadores económicos y pagos ajustados — paso 3.1.1."""
from dominio.deserializador_indicador import DeserializadorIndicador
from dominio.permisos import exigir_admin, exigir_sesion
from persistencia.indicador_dao import IndicadorDAO
from registro_errores import log
from servicios.api_dolar import obtener_datos
from servicios.http_cliente import ErrorServicioExterno


def consultar_indicador(sesion, dao=None):
    """Consulta el dólar en la API, lo valida y guarda el historial."""
    exigir_sesion(sesion)
    datos = obtener_datos()
    try:
        indicador = DeserializadorIndicador.desde_api(datos)
    except (ValueError, TypeError):
        log.error("La API del dólar devolvió datos con formato inesperado")
        raise ErrorServicioExterno("La respuesta del servicio no contiene un indicador válido.")

    try:
        (dao or IndicadorDAO()).guardar(indicador)
    except Exception:
        # Guardar el historial es secundario: si falla, igual se muestra el valor.
        log.exception("No se pudo guardar el indicador en la base de datos")
    return indicador


def obtener_historial(sesion, dao=None, limite=10):
    exigir_sesion(sesion)
    return (dao or IndicadorDAO()).obtener_historial("dolar", limite)


def calcular_pago_usd(sesion, salario_clp, dao=None):
    """Convierte un salario en CLP a USD con el dólar actualizado (solo admin)."""
    exigir_admin(sesion)
    salario = float(salario_clp)
    if salario <= 0:
        raise ValueError("El salario debe ser mayor que 0.")
    indicador = consultar_indicador(sesion, dao)
    return {
        "salario_clp": round(salario, 2),
        "dolar": indicador.valor,
        "fecha_dolar": str(indicador.fecha)[:10],
        "pago_usd": round(salario / indicador.valor, 2),
    }
