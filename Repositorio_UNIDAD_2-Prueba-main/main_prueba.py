import requests

def obtener_datos():
    respuesta = requests.get(
    #"https://mindicador.cl/api/dolar",
    "https://open.er-api.com/v6/latest/USD",
        timeout=(3, 5),
    )
    print("Estado HTTP:", respuesta.status_code)
    respuesta.raise_for_status()
    return respuesta.json()

import math
import math
import requests

def obtener_datos():
    """Realiza la petición HTTP para obtener los datos del indicador."""
    respuesta = requests.get(
        "https://mindicador.cl/api/dolar",  
        timeout=(3, 5),
    )
    print("Estado HTTP:", respuesta.status_code)
    respuesta.raise_for_status()
    return respuesta.json()

def extraer_primero(datos):
    """
    Comprueba que la serie tenga datos, valida que el valor sea numérico,
    finito y positivo, y muestra la fecha del registro utilizado.
    """
    
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada: se esperaba un diccionario.")


    serie = datos.get("serie")
    
   
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles en la serie.")

    
    registro = serie[0]
    if not isinstance(registro, dict):
        raise ValueError("El formato del registro es inválido.")

   
    if "valor" not in registro or "fecha" not in registro:
        raise ValueError("El registro no contiene las claves 'valor' o 'fecha'.")

    valor = registro["valor"]
    fecha = registro["fecha"]


    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        raise ValueError("El valor del indicador debe ser de tipo numérico.")
    
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError("El valor del indicador debe ser un número finito y mayor que cero.")


    print(f"Registro utilizado - Fecha: {fecha} | Valor: {valor}")

   
    return fecha, valor



if __name__ == "__main__":
    try:
        datos_api = obtener_datos()
        fecha_utilizada, valor_utilizado = extraer_primero(datos_api)
    except Exception as e:
        print(f"Ocurrió un error: {e}")

try:
    
    datos = obtener_datos()
    
    
    fecha, valor = extraer_primero(datos)
    
    
    print(f"Dólar observado: {valor:.2f} CLP por USD")
    
    
    print(f"Fecha del registro: {fecha}")
except requests.exceptions.RequestException:
    print("No pudimos consultar el servicio. Reintente.")

except (ValueError, KeyError, TypeError):
    print("La respuesta no contiene un indicador válido.")

