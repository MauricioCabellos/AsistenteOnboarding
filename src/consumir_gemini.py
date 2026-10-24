import os
import requests
from dotenv import load_dotenv

import time #importar librería de tiempo para calcular latencia

import json
import re

load_dotenv()

#Variables constantes, son las que no cambian
MODELO = "gemini-3.5-flash-lite"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#función para crear la solicitud
def armar_peticion(modelo, pregunta, system_instruction, response_schema=None):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    url = f"{URL_BASE}{modelo}:generateContent?key={API_KEY}"
    body = {
            "systemInstruction": {
                "parts": [ {"text": system_instruction} ]
            },
            "contents": 
                [{"parts": [{"text": pregunta}]}]
        }
    
    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
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

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "categoria": {"type": "STRING"},
            "confianza": {"type": "NUMBER"},
        },
        "required": ["categoria", "confianza"]
    }
    system_instruction = "Eres un asistente amigable y respondes en máximo 2 palabras."
    url, body = armar_peticion("gemini-3.5-flash", pregunta, system_instruction, response_schema)

    inicio = time.perf_counter()  # Inicia el temporizador

    datos = enviar_peticion(url, body)

    fin = time.perf_counter()  # Finaliza el temporizador
    latencia = fin - inicio  # Calcula la latencia
    print(f"Latencia: {latencia:.2f} segundos") # Imprime la latencia en segundos

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    texto = extraer_texto(datos) 
    datos_formateados = parsear_respuesta_json(texto, ["categoria", "confianza"])
    return datos_formateados

#Calcular Costos
def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso["thoughtsTokenCount"]
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo

def parsear_respuesta_json(texto, claves_requeridas=None):
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es un JSON válido.")

    if claves_requeridas:
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError("La respuesta no tiene la estructura esperada.")

    return datos

try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexion funciona"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)

