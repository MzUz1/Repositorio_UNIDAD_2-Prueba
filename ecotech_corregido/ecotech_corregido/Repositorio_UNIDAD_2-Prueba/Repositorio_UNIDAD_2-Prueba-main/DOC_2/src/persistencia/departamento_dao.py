from persistencia.conexion import abrir_conexion
from persistencia.interfaces_dao import IDepartamentoDAO


class DepartamentoDAO(IDepartamentoDAO):
    def insertar(self, departamento):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO departamento (nombre) VALUES (%s)", (departamento.nombre,))
            conexion.commit()
            departamento.id_departamento = cursor.lastrowid
            return departamento
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def obtener_por_id(self, id_departamento):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_departamento, nombre, id_gerente FROM departamento WHERE id_departamento=%s", (id_departamento,))
            fila = cursor.fetchone()
            return self._fila_a_dict(fila) if fila else None
        finally:
            cursor.close()
            conexion.close()

    def obtener_todos(self):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_departamento, nombre, id_gerente FROM departamento ORDER BY id_departamento")
            return [self._fila_a_dict(fila) for fila in cursor.fetchall()]
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, id_departamento, departamento):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE departamento SET nombre=%s WHERE id_departamento=%s", (departamento.nombre, id_departamento))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id_departamento):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM departamento WHERE id_departamento=%s", (id_departamento,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def agregar_empleado(self, id_empleado, id_departamento):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE empleado SET id_departamento=%s WHERE id_empleado=%s", (id_departamento, id_empleado))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def remover_empleado(self, id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE empleado SET id_departamento=NULL WHERE id_empleado=%s", (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def asignar_gerente(self, id_departamento, id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE departamento SET id_gerente=%s WHERE id_departamento=%s", (id_empleado, id_departamento))
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
        return {"id_departamento": fila[0], "nombre": fila[1], "id_gerente": fila[2]}
