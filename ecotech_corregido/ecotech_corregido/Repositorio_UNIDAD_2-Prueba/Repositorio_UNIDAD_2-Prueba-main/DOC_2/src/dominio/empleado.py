
from datetime import date


class Empleado:
    def __init__(
        self,
        nombre,
        direccion,
        telefono,
        correo,
        fecha_inicio_contrato,
        salario,
        id_empleado=None,
        id_departamento=None,
    ):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario
        self.id_departamento = id_departamento

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La dirección no puede estar vacía.")
        self.__direccion = valor.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El teléfono no puede estar vacío.")
        self.__telefono = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor:
            raise ValueError("El correo no es válido.")
        self.__correo = valor.strip()

    @property
    def fecha_inicio_contrato(self):
        return self.__fecha_inicio_contrato

    @fecha_inicio_contrato.setter
    def fecha_inicio_contrato(self, valor):
        if not isinstance(valor, date):
            raise ValueError("La fecha debe ser un objeto date.")
        self.__fecha_inicio_contrato = valor

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise ValueError("El salario no puede ser negativo.")
        self.__salario = valor

    def registrar_empleado(self):
        return True

    def actualizar_datos(
        self,
        nombre,
        direccion,
        telefono,
        correo,
        fecha_inicio_contrato,
        salario,
    ):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

    def registrar_horas(self):
        return True

    def obtener_permisos(self):
        return []

