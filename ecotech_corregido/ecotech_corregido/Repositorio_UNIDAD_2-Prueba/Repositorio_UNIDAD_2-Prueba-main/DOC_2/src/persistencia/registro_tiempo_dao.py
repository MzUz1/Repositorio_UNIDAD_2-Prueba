from persistencia.conexion import abrir_conexion
from persistencia.interfaces_dao import IRegistroTiempoDAO


class RegistroTiempoDAO(IRegistroTiempoDAO):
    def insertar(self, registro):
        registro.validar_registro()
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO registro_tiempo
                (id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion_trabajo)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                registro.id_empleado,
                registro.id_proyecto,
                registro.fecha,
                registro.horas_trabajadas,
                registro.descripcion_trabajo,
            ))
            conexion.commit()
            registro.id_registro = cursor.lastrowid
            return registro
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def obtener_por_id(self, id_registro):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                SELECT id_registro, id_empleado, id_proyecto, fecha,
                       horas_trabajadas, descripcion_trabajo
                FROM registro_tiempo
                WHERE id_registro=%s
            """, (id_registro,))
            fila = cursor.fetchone()
            return self._fila_a_dict(fila) if fila else None
        finally:
            cursor.close()
            conexion.close()

    def obtener_todos(self):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                SELECT id_registro, id_empleado, id_proyecto, fecha,
                       horas_trabajadas, descripcion_trabajo
                FROM registro_tiempo
                ORDER BY fecha DESC, id_registro DESC
            """)
            return [self._fila_a_dict(fila) for fila in cursor.fetchall()]
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, id_registro, registro):
        registro.validar_registro()
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                UPDATE registro_tiempo
                SET id_empleado=%s, id_proyecto=%s, fecha=%s,
                    horas_trabajadas=%s, descripcion_trabajo=%s
                WHERE id_registro=%s
            """, (
                registro.id_empleado, registro.id_proyecto, registro.fecha,
                registro.horas_trabajadas,
                registro.descripcion_trabajo, id_registro
            ))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id_registro):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM registro_tiempo WHERE id_registro=%s", (id_registro,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def obtener_todos_con_detalles(self):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                SELECT r.id_registro, r.fecha, e.nombre, p.nombre,
                       r.horas_trabajadas, r.descripcion_trabajo
                FROM registro_tiempo r
                INNER JOIN empleado e ON r.id_empleado = e.id_empleado
                INNER JOIN proyecto p ON r.id_proyecto = p.id_proyecto
                ORDER BY r.fecha DESC, r.id_registro DESC
            """)
            return [
                {
                    "id_registro": fila[0],
                    "fecha": fila[1],
                    "empleado": fila[2],
                    "proyecto": fila[3],
                    "horas": fila[4],
                    "descripcion": fila[5],
                }
                for fila in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def _fila_a_dict(fila):
        return {
            "id_registro": fila[0],
            "id_empleado": fila[1],
            "id_proyecto": fila[2],
            "fecha": fila[3],
            "horas_trabajadas": fila[4],
            "descripcion_trabajo": fila[5],
        }
