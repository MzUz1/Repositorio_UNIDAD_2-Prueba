
from persistencia.conexion import abrir_conexion
from persistencia.interfaces_dao import IEmpleadoDAO


class EmpleadoDAO(IEmpleadoDAO):

    def insertar(self, empleado):
        conexion = abrir_conexion()
        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO empleado
                (nombre, direccion, telefono, correo,
                 fecha_inicio_contrato, salario, id_departamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                empleado.nombre,
                empleado.direccion,
                empleado.telefono,
                empleado.correo,
                empleado.fecha_inicio_contrato,
                empleado.salario,
                empleado.id_departamento,
            ))

            conexion.commit()
            empleado.id_empleado = cursor.lastrowid
            return empleado

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def obtener_por_id(self, id_empleado):
        conexion = abrir_conexion()
        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM empleado WHERE id_empleado = %s",
                (id_empleado,),
            )
            fila = cursor.fetchone()

            return self._fila_a_dict(fila) if fila else None

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def obtener_todos(self):
        conexion = abrir_conexion()
        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM empleado ORDER BY id_empleado"
            )

            return [
                self._fila_a_dict(fila)
                for fila in cursor.fetchall()
            ]

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def actualizar(self, id_empleado, empleado):
        conexion = abrir_conexion()
        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE empleado
                SET nombre = %s,
                    direccion = %s,
                    telefono = %s,
                    correo = %s,
                    fecha_inicio_contrato = %s,
                    salario = %s,
                    id_departamento = %s
                WHERE id_empleado = %s
            """, (
                empleado.nombre,
                empleado.direccion,
                empleado.telefono,
                empleado.correo,
                empleado.fecha_inicio_contrato,
                empleado.salario,
                empleado.id_departamento,
                id_empleado,
            ))

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def eliminar(self, id_empleado):
        conexion = abrir_conexion()
        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute(
                "DELETE FROM empleado WHERE id_empleado = %s",
                (id_empleado,),
            )

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    @staticmethod
    def _fila_a_dict(fila):
        return {
            "id_empleado": fila[0],
            "nombre": fila[1],
            "direccion": fila[2],
            "telefono": fila[3],
            "correo": fila[4],
            "fecha_inicio_contrato": fila[5],
            "salario": fila[6],
            "id_departamento": fila[7],
        }
