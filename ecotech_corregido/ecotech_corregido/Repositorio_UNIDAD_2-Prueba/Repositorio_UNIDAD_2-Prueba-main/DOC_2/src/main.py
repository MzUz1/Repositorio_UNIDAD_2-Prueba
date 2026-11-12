from dominio.menu_usuario import iniciar_sesion_con_intentos
from persistencia.crear_db import crear_base_y_tablas
from persistencia.dao_factory import DAOFactory
from registro_errores import log
from ux.interfaz import TerminalInterface


def main():
    try:
        crear_base_y_tablas()
    except ConnectionError as e:
        print(e)
        return
    except Exception:
        log.exception("Error al preparar la base de datos")
        print("No se pudo preparar la base de datos. Revise la configuración.")
        return

    # Control de acceso: sin sesión válida no se muestra el menú
    sesion = iniciar_sesion_con_intentos()
    if sesion is None:
        return

    try:
        factory = DAOFactory()
        app = TerminalInterface(
            factory.get_registro_tiempo_dao(),
            factory.get_empleado_dao(),
            factory.get_proyecto_dao(),
            factory.get_departamento_dao(),
            sesion=sesion,
        )
        app.iniciar()
    except Exception:
        log.exception("Error al iniciar el sistema")
        print("Error al iniciar el sistema. Revise errores.log.")


if __name__ == "__main__":
    main()
