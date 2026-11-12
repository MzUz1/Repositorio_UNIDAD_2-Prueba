"""Crea el primer administrador. Ejecutar UNA vez:  python crear_admin.py

Si todavía no hay ningún empleado, también lo registra (el menú exige
iniciar sesión, así que el primer empleado no se puede crear desde ahí).
"""
from getpass import getpass

from dominio.empleado import Empleado
from dominio.entradas import pedir_dato
from dominio.usuario import Usuario
from persistencia.crear_db import crear_base_y_tablas
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autenticacion import registrar_usuario
from ux.interfaz import TerminalInterface


def _crear_empleado_inicial():
    print("\n--- DATOS DEL EMPLEADO ADMINISTRADOR ---")
    empleado = Empleado(
        input("Nombre: ").strip(),
        input("Dirección: ").strip(),
        input("Teléfono: ").strip(),
        input("Correo: ").strip(),
        TerminalInterface._pedir_fecha("Fecha de inicio (YYYY-MM-DD): "),
        TerminalInterface._pedir_float("Salario: "),
    )
    EmpleadoDAO().insertar(empleado)
    print(f"Empleado creado con ID {empleado.id_empleado}.")
    return empleado.id_empleado


def main():
    crear_base_y_tablas()
    try:
        if input("¿El empleado administrador ya existe? (s/n): ").strip().lower() == "s":
            empleado_id = pedir_dato("ID del empleado: ", int)
        else:
            empleado_id = _crear_empleado_inicial()

        nombre = pedir_dato("Usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden.")
            return
        registrar_usuario(empleado_id, nombre, clave, rol="admin")
    except (TypeError, ValueError) as error:
        print(error)
        return
    print("Administrador creado correctamente.")


if __name__ == "__main__":
    main()
