import requests
respuesta = requests.get(
"https://mindicador.cl/api/dolar",
timeout=(3, 5),
)
print("Estado HTTP:", respuesta.status_code)