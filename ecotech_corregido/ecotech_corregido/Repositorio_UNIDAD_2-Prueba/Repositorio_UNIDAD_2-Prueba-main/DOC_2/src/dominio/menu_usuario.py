from getpass import getpass

from dominio.entradas import pedir_dato
from dominio.permisos import exigir_admin
from dominio.usuario import Usuario
from servicios.autenticacion import autenticar, registrar_usuario

MAX_INTENTOS = 3


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")
    print(f"Rol: {usuario_actual['rol']}")


def solicitar_registro(usuario_actual):
    """Crea una cuenta nueva (rol empleado). Solo la puede usar un administrador."""
    exigir_admin(usuario_actual)
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None

        usuario_id = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(error)
        return None

    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None

    if usuario is None:
        print("Usuario o contraseña incorrectos.")
        return None

    print("Sesión iniciada correctamente.")
    return usuario


def iniciar_sesion_con_intentos(max_intentos=MAX_INTENTOS):
    """Pide credenciales hasta max_intentos veces. Devuelve la sesión o None."""
    print("\n=== ECOTECH SOLUTIONS - Inicio de sesión ===")
    for intento in range(1, max_intentos + 1):
        usuario = solicitar_login()
        if usuario is not None:
            return usuario
        print(f"Intento {intento} de {max_intentos}.")
    print("Demasiados intentos fallidos.")
    return None
