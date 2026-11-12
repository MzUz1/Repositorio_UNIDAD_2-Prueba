class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio, id_proyecto=None):
        self.id_proyecto = id_proyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
        self._empleados = []

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self.__descripcion = valor.strip()

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        self.__fecha_inicio = valor

    @property
    def empleados(self):
        return tuple(self._empleados)

    def crear_proyecto(self):
        return True

    def editar_proyecto(self, nombre, descripcion, fecha_inicio):
        self.actualizar_datos(nombre, descripcion, fecha_inicio)

    def eliminacion_proyecto(self):
        return self.id_proyecto

    def asignar_empleado(self, empleado):
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            return True
        return False

    def desasignar_empleado(self, empleado):
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            return True
        return False

    def actualizar_datos(self, nombre, descripcion, fecha_inicio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
