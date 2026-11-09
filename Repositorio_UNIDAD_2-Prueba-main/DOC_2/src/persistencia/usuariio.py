@classmethod
def normalizar_usuario(cls, nombre):
if not isinstance(nombre, str):
raise TypeError("El usuario debe ser texto.")
nombre = nombre.strip().lower()
if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
raise ValueError("Usuario fuera del largo permitido.")
if not all(c.isascii() and (c.isalnum() or c == "_")
for c in nombre):
raise ValueError("Use letras ASCII, números o guion bajo.")
return nombre