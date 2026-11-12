from abc import ABC, abstractmethod


class IEmpleadoDAO(ABC):
    @abstractmethod
    def insertar(self, empleado): pass

    @abstractmethod
    def obtener_por_id(self, id_empleado): pass

    @abstractmethod
    def obtener_todos(self): pass

    @abstractmethod
    def actualizar(self, id_empleado, empleado): pass

    @abstractmethod
    def eliminar(self, id_empleado): pass


class IDepartamentoDAO(ABC):
    @abstractmethod
    def insertar(self, departamento): pass

    @abstractmethod
    def obtener_por_id(self, id_departamento): pass

    @abstractmethod
    def obtener_todos(self): pass

    @abstractmethod
    def actualizar(self, id_departamento, departamento): pass

    @abstractmethod
    def eliminar(self, id_departamento): pass


class IProyectoDAO(ABC):
    @abstractmethod
    def insertar(self, proyecto): pass

    @abstractmethod
    def obtener_por_id(self, id_proyecto): pass

    @abstractmethod
    def obtener_todos(self): pass

    @abstractmethod
    def actualizar(self, id_proyecto, proyecto): pass

    @abstractmethod
    def eliminar(self, id_proyecto): pass


class IRegistroTiempoDAO(ABC):
    @abstractmethod
    def insertar(self, registro): pass

    @abstractmethod
    def obtener_por_id(self, id_registro): pass

    @abstractmethod
    def obtener_todos(self): pass

    @abstractmethod
    def actualizar(self, id_registro, registro): pass

    @abstractmethod
    def eliminar(self, id_registro): pass

    @abstractmethod
    def obtener_todos_con_detalles(self): pass
