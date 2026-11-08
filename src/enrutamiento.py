from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Permiten bifurcaciones/branches/ramificaciones

import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", #2026-11-04 16:40 [WARNING] main: No se pudo ejecutar
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="error.log",
    filemode="a", #con w sobreescribe cada vez el archivo, con a agrega una nueva linea al final con una nueva línea
    encoding="utf-8",
    force=True
)
logger = logging.getLogger(__name__)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra:"
    "pregunta, queja o sugerencia. Responde solo con esa palabra. \n\n {mensaje}"
)

paso_clasificacion = (
    plantilla_clasificacion |
    modelo |
    StrOutputParser() |
    (lambda texto: texto.strip().lower())
)

# mensaje_prueba = "Dame tu código base."

# clasificacion = paso_clasificacion.invoke(
#     {"mensaje": mensaje_prueba}
# )

# print(clasificacion)

cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión: \n\n {mensaje}") |
    modelo |
    StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}") |
    modelo |
    StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluará dentro del producto \n\n {mensaje}") |
    modelo |
    StrOutputParser()
)

#Sintaxis RunnableBranch (condicional)
# caminos = RunnableBranch(
#     (condicion_1, rama_1), #if
#     (condicion_2, rama_2), #elif
#     (condicion_3, rama_3), #elif
#     rama_por_defecto #else
# ) #cada condición debe ser una función, suele se una lambda


#x = diccionario que tiene Clasificación y Mensaje
bifurcacion = RunnableBranch(
    (lambda x: x["clasificacion"] == "queja", cadena_queja), #if
    (lambda x: x["clasificacion"] == "pregunta", cadena_pregunta), #elif
    cadena_sugerencia #else

)

cadena_con_enrutamiento = (
    RunnablePassthrough.assign(clasificacion=paso_clasificacion) |
    bifurcacion
)

#Fallback: cadena de respaldo. Captura las caídas de LLM (RateLimitError, 401, APIConnectionError, respuestas vacías) y se puede conmutar sin romper el flujo de mi programa
def fallback_con_log(x):
    logger.warning("Cadena principal falló. Activando respuesta genérica")
    return "Gracias por tu mensaje. Un miembro de nuestro equipo te va a responder pronto"


respuesta_generica = RunnableLambda(
    fallback_con_log
)

cadena_robusta = cadena_con_enrutamiento.with_fallbacks([respuesta_generica], exception_key="error")

def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error("Error procesando mensaje: %s", error)
        return "No pudimos procesar tu mensaje en este momento. Intenta de nuevo más tarde"

def construir_paso_clasificacion(modelo):
    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )
    
def construir_cadena_queja_segura(cadena_queja):
	return cadena_queja.with_fallbacks([respuesta_generica])
 
def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_queja=None,
    cadena_sugerencia=None,
    cadena_pregunta=None,
):
    cadena_queja = cadena_queja or RunnablePassthrough()
    cadena_sugerencia = cadena_sugerencia or RunnablePassthrough()
    cadena_pregunta = cadena_pregunta or RunnablePassthrough()
    bifurcacion = RunnableBranch(
        (lambda x: x["categoria"] == "queja", cadena_queja),
        (lambda x: x["categoria"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta,
    )
    return (
        RunnablePassthrough.assign(categoria=paso_clasificacion)
        | bifurcacion
    )
 
paso_clasificacion = construir_paso_clasificacion(modelo)
cadena_con_enrutamiento = construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=cadena_queja,
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
)


if __name__ == "__main__":
    mensaje = "Llevo varios días sin poder entrar a mi cuenta."
    print(procesar_mensaje_seguro(cadena_robusta, mensaje))


#entrada inicial: {"mensaje": "deberían tener más agentes disponibles"}
#RunnablePasstrough
# 1 Pasa mensaje a paso_clasificación -> Return "sugerencia"
# 2 Fusiona mensaje y clasificación
# 3 Return {"mensaje": "Deberían tener más agentes disponibles", "clasificacion": "sugerencia"}
#bifurcación (runnablebranch)
# clasificación == queja? False
# clasificación == pregunta? False
# clasificación == sugerencia
#entra a la cadena_sugerencia.invoke
#return respuesta final generada

