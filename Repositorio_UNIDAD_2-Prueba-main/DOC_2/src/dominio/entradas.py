def pedir_dato(mensaje, validador, leer=input):
    while True:
        try:
            return validador(leer(mensaje))
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")