from datetime import datetime

from persistencia.conexion import abrir_conexion

SQL_GUARDAR = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    valor = VALUES(valor),
    unidad = VALUES(unidad),
    verificado_en = VALUES(verificado_en)
"""

SQL_HISTORIAL = """
SELECT fecha, valor, unidad, fuente, verificado_en
FROM indicador_api
WHERE codigo = %s
ORDER BY fecha DESC
LIMIT %s
"""


class IndicadorDAO:
    def guardar(self, indicador):
        # La API entrega fechas como '2026-11-11T03:00:00.000Z': se guarda solo el día.
        fecha = datetime.strptime(str(indicador.fecha)[:10], "%Y-%m-%d").date()
        verificado = indicador.verificado_en or datetime.now()

        conexion = abrir_conexion()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(SQL_GUARDAR, (
                indicador.fuente, indicador.codigo, fecha,
                indicador.valor, indicador.unidad, verificado,
            ))
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def obtener_historial(self, codigo="dolar", limite=10):
        conexion = abrir_conexion()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(SQL_HISTORIAL, (codigo, int(limite)))
            return [
                {"fecha": f[0], "valor": float(f[1]), "unidad": f[2],
                 "fuente": f[3], "verificado_en": f[4]}
                for f in cursor.fetchall()
            ]
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
