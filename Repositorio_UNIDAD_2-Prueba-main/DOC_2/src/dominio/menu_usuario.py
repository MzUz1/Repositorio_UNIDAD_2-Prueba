from getpass import getpass

from dominio.entradas import pedir_dato
from dominio.usuario import Usuario
from servicios.autenticacion import autenticar, registrar_usuario


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")


def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    print("Consulta de indicadores disponible.")


def solicitar_registro():
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


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"

    while True:
        print("1 Registrar, 2 Perfil, 3 Indicador, 9 Cerrar sesión, 0 Salir")
        opcion = input("Opción: ").strip()

        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            solicitar_registro()
        elif opcion == "2":
            mostrar_perfil(usuario_actual)
        elif opcion == "3":
            consultar_indicador(usuario_actual)
        else:
            print("Opción no válida.")

