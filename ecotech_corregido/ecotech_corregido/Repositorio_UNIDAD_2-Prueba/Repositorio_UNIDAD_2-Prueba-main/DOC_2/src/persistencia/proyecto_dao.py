from persistencia.conexion import abrir_conexion
from persistencia.interfaces_dao import IProyectoDAO


class ProyectoDAO(IProyectoDAO):
    def insertar(self, proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
                VALUES (%s, %s, %s)
            """, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
            conexion.commit()
            proyecto.id_proyecto = cursor.lastrowid
            return proyecto
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def obtener_por_id(self, id_proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_proyecto, nombre, descripcion, fecha_inicio FROM proyecto WHERE id_proyecto=%s", (id_proyecto,))
            fila = cursor.fetchone()
            return self._fila_a_dict(fila) if fila else None
        finally:
            cursor.close()
            conexion.close()

    def obtener_todos(self):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_proyecto, nombre, descripcion, fecha_inicio FROM proyecto ORDER BY id_proyecto")
            return [self._fila_a_dict(fila) for fila in cursor.fetchall()]
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, id_proyecto, proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                UPDATE proyecto
                SET nombre=%s, descripcion=%s, fecha_inicio=%s
                WHERE id_proyecto=%s
            """, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, id_proyecto))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id_proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM proyecto WHERE id_proyecto=%s", (id_proyecto,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def asignar_empleado(self, id_proyecto, id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO empleado_proyecto (id_empleado, id_proyecto)
                VALUES (%s, %s)
            """, (id_empleado, id_proyecto))
            conexion.commit()
            return True
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def desasignar_empleado(self, id_proyecto, id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM empleado_proyecto WHERE id_proyecto=%s AND id_empleado=%s", (id_proyecto, id_empleado))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def _fila_a_dict(fila):
        return {"id_proyecto": fila[0], "nombre": fila[1], "descripcion": fila[2], "fecha_inicio": fila[3]}
