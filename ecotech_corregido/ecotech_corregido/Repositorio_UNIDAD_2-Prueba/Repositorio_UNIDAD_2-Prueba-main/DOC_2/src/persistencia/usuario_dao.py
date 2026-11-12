import mysql.connector

from persistencia.conexion import abrir_conexion
from dominio.usuario import Usuario

# Columnas por las que se permite buscar (lista blanca: nunca se arma SQL con texto externo)
_COLUMNAS_BUSQUEDA = {"username": "username", "id_empleado": "id_empleado"}


class UsuarioDAO:

    def insertar(self, usuario):
        conexion = abrir_conexion()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO usuario (username, password_hash, rol, id_empleado)
                VALUES (%s, %s, %s, %s)
            """, (usuario.nombre_usuario, usuario.password_hash,
                  usuario.rol, usuario.empleado_id))
            conexion.commit()
            usuario.id = cursor.lastrowid
            return usuario.id
        except mysql.connector.IntegrityError:
            conexion.rollback()
            raise ValueError(
                "No se pudo crear la cuenta. Verifique que el empleado exista "
                "y que no tenga ya una cuenta."
            )
        except Exception:
            conexion.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def buscar_por_nombre(self, nombre_usuario):
        return self._buscar("username", nombre_usuario)

    def buscar_por_empleado(self, id_empleado):
        return self._buscar("id_empleado", id_empleado)

    def _buscar(self, columna, valor):
        columna_sql = _COLUMNAS_BUSQUEDA[columna]
        conexion = abrir_conexion()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id_usuario, username, password_hash, id_empleado, rol, activo "
                f"FROM usuario WHERE {columna_sql} = %s",
                (valor,),
            )
            fila = cursor.fetchone()
            # Sin empleado asociado o cuenta desactivada: no puede iniciar sesión
            if fila is None or fila[3] is None or not fila[5]:
                return None
            return Usuario(nombre_usuario=fila[1], password_hash=fila[2],
                           empleado_id=fila[3], id=fila[0], rol=fila[4])
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
