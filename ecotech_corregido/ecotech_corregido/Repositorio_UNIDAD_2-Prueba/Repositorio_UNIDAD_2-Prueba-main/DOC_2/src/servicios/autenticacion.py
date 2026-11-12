import bcrypt

from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO
from registro_errores import log

MAX_BYTES_BCRYPT = 72
_hash_falso = None


def _hash_para_comparar_en_falso():
    """Hash de relleno: así tarda lo mismo si el usuario existe o no."""
    global _hash_falso
    if _hash_falso is None:
        _hash_falso = bcrypt.hashpw(b"relleno-no-valido", bcrypt.gensalt())
    return _hash_falso


def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


def registrar_usuario(empleado_id, nombre, clave, rol="empleado"):
    nombre = Usuario.normalizar_usuario(nombre)
    Usuario.validar_rol(rol)
    dao = UsuarioDAO()

    if dao.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")

    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id, rol=rol)
    return dao.insertar(usuario)


def autenticar(nombre, clave):
    """Devuelve la sesión (dict con rol) o None. Nunca dice qué dato falló."""
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None

    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None

    cuenta = UsuarioDAO().buscar_por_nombre(nombre)

    if cuenta is None:
        bcrypt.checkpw(datos, _hash_para_comparar_en_falso())
        log.error("Intento de login con usuario inexistente o inactivo: %s", nombre)
        return None

    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        log.error("Clave incorrecta para el usuario: %s", nombre)
        return None

    return {
        "id": cuenta.id,
        "empleado_id": cuenta.empleado_id,
        "nombre_usuario": cuenta.nombre_usuario,
        "rol": cuenta.rol,
    }
