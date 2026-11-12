class Departamento:
    def __init__(self, nombre, id_departamento=None, id_gerente=None):
        self.id_departamento = id_departamento
        self.__nombre = nombre
        self.id_gerente = id_gerente
        self._empleados = []

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def empleados(self):
        return tuple(self._empleados)

    def agregar_empleado(self, empleado):
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            return True
        return False

    def remover_empleado(self, empleado):
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            return True
        return False

    def asignar_gerente(self, empleado):
        self.id_gerente = empleado.id_empleado

    def creacion_departamento(self):
        return True

    def editar_departamento(self, nombre):
        self.nombre = nombre

    def busqueda_departamento(self):
        return self.id_departamento

    def eliminacion_departamento(self):
        return self.id_departamento

    def actualizar_datos(self, nombre):
        self.nombre = nombre
