import os
import requests
from dotenv import load_dotenv

import time #importar librería de tiempo para calcular latencia

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

    inicio = time.perf_counter()  # Inicia el temporizador

    datos = enviar_peticion(url, body)

    fin = time.perf_counter()  # Finaliza el temporizador
    latencia = fin - inicio  # Calcula la latencia
    print(f"Latencia: {latencia:.2f} segundos") # Imprime la latencia en segundos

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    return extraer_texto(datos) 

#Calcular Costos
def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso["thoughtsTokenCount", 0]
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo

try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexion funciona"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)
#Ejecutar 4 veces la misma petición con un modelo, y ante cada petición se calcule e imprima: Latencia, costo y respuesta. 
#Luego vuelvo a hacer lo mismo con otros modelos, idealmente 3 modelos a comparar. De esta forma elegir el modelo óptimo para mi proyecto.
#Prompt debe ser algo relacionado con el proyecto.

#SCRIPT PARA COMPARAR MODELOS

#Definimos los 3 modelos a comparar
precios_modelos = {
    "gemini-3.6-flash": {
        "entrada": 0.000000075, 
        "salida": 0.000000300   
    },
    "gemini-3.5-flash-lite": {
        "entrada": 0.000000035, # Tarifa estimada para versión Lite
        "salida": 0.000000150
    },
    "gemini-3.1-flash-lite": {
        "entrada": 0.000000015, # Tarifa estimada para versión Lite antigua
        "salida": 0.000000075
    }
}

iteraciones = 4
prompt_proyecto = "Define qué es el proceso de onboarding en una empresa en exactamente una oración."

# 2. Sobrescribimos el cálculo de costo para manejar tokens de razonamiento opcionales de forma segura
def calcular_costo_seguro(datos, precio_entrada, precio_salida):
    uso = datos.get("usageMetadata", {})
    tokens_entrada = uso.get("promptTokenCount", 0)
    tokens_salida = uso.get("candidatesTokenCount", 0)
    # Si el modelo no tiene razonamiento, usa 0 en vez de romper la ejecución
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0)
    
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo

# 3. Función de prueba adaptada
def obtener_dato_con_precio_dinamico(pregunta, precio_in, precio_out):
    url, body = armar_peticion(pregunta)

    inicio = time.perf_counter()
    datos = enviar_peticion(url, body)
    fin = time.perf_counter()
    
    latencia = fin - inicio
    print(f"Latencia: {latencia:.2f} segundos")

    costo = calcular_costo_seguro(datos, precio_in, precio_out)
    print(f"Costo de la petición: ${costo:.6f} USD")
    
    return extraer_texto(datos)

print("\n" + "="*60)
print(" INICIANDO COMPARATIVA DE MODELOS ".center(60, "="))
print("="*60)

# 4. Bucle de ejecución
for modelo_actual, tarifas in precios_modelos.items():
    MODELO = modelo_actual
    
    print(f"\n🚀 Evaluando modelo: {MODELO}")
    print(f"Tarifa Entrada: ${tarifas['entrada']} | Tarifa Salida: ${tarifas['salida']}")
    print("-" * 60)
    
    for i in range(1, iteraciones + 1):
        print(f"--- Iteración {i}/{iteraciones} ---")
        try:
            respuesta = obtener_dato_con_precio_dinamico(
                prompt_proyecto, 
                tarifas["entrada"], 
                tarifas["salida"]
            )
            print(f"Respuesta:\n{respuesta}")
        except (ValueError, RuntimeError) as error:
            print(f"Error en la ejecución: {error}")
        
        print("." * 40)
        time.sleep(2)