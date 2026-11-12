class RegistroTiempo:
    def __init__(self, fecha, horas_trabajadas, descripcion_trabajo, id_empleado, id_proyecto, id_registro=None):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_trabajo = descripcion_trabajo
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    def registrar_tiempo(self):
        self.validar_registro()
        return True

    def validar_registro(self):
        if self.horas_trabajadas <= 0 or self.horas_trabajadas > 24:
            raise ValueError("Las horas trabajadas deben estar entre 0 y 24.")
        if not self.descripcion_trabajo.strip():
            raise ValueError("La descripción del trabajo no puede estar vacía.")
        return True

    def actualizar_registro(self, fecha, horas_trabajadas, descripcion_trabajo):
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_trabajo = descripcion_trabajo
        self.validar_registro()
