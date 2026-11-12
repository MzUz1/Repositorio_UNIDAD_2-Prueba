from .empleado_dao import EmpleadoDAO
from .departamento_dao import DepartamentoDAO
from .proyecto_dao import ProyectoDAO
from .registro_tiempo_dao import RegistroTiempoDAO


class DAOFactory:
    """Fábrica de DAOs. El proyecto usa exclusivamente MySQL."""

    def __init__(self):
        self._empleado_dao = EmpleadoDAO()
        self._departamento_dao = DepartamentoDAO()
        self._proyecto_dao = ProyectoDAO()
        self._registro_tiempo_dao = RegistroTiempoDAO()

    def get_empleado_dao(self):
        return self._empleado_dao

    def get_departamento_dao(self):
        return self._departamento_dao

    def get_proyecto_dao(self):
        return self._proyecto_dao

    def get_registro_tiempo_dao(self):
        return self._registro_tiempo_dao
