import os
import requests
from dotenv import load_dotenv

load_dotenv()

#Variables constantes, son las que no cambian
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#función para crear la solicitud
def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
    body = {
        "contents": 
        [{"parts": [{"text": pregunta}]}]
    }
    return url, body

#función envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos momentos")
    except requests.exceptions.Timeout:
        raise RuntimeError("Se agotó el tiempo de espera para la solicitud. Intenta de nuevo en unos momentos")

    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la petición. Status code: {respuesta.status_code}")

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado")

#función procesa y extrae dato
def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La estructura de la respuesta no es la esperada")

#función recibe la pregunta y devuelve los resultados
def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    return extraer_texto(datos) 

#Calcular Costos
def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]
    '''
    uso = {
        "promptTokenCount": 15,
            "candidatesTokenCount": 457,
            "totalTokenCount": 1214,
            "promptTokensDetails": [
                {
                    "modality": "TEXT",
                    "tokenCount": 15
                }
            ],
            "thoughtsTokenCount": 742,
            "serviceTier": "standard"
    }
    '''
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso["thoughtsTokenCount"]
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo

try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexion funciona"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)