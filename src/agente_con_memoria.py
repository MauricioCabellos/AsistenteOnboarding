#Herramientas Personalizadas
#Intro a Memoria

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.prompts import(ChatPromptTemplate, MessagesPlaceholder)
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import(AgentExecutor, create_tool_calling_agent)
from pydantic import BaseModel, Field, ValidationError
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

#Configuraciones e Inicializaciones
load_dotenv()
modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

class ArgumentosConsultaEnvio(BaseModel):
    """
    Esquema para documentar y validar argumentos campo por campo ante el LLM.
    """
    numero_seguimiento: str = Field(
        description="Número de seguimiento del envío, por ejemplo 'AR129012'."
    )
    incluir_historial: bool = Field(
        default=False,
        description="Si es True, incluye el historial completo de los estados, no solo el actual."
    )

ESTADOS = {
    "AR12345": {
        "actual": "En tránsito. Entrega estimada de 2 días.",
        "historial":[
            "Recibido en depósito",
            "En tránsito"
        ]
    },
    "AR67890": {
            "actual": "Entregado.",
            "historial":[
                "Recibido en depósito",
                "En tránsito"
            ]
        }
}

#Herramientas
#@tool("nuevo_nombre_del_tool")
@tool(args_schema=ArgumentosConsultaEnvio) #LangChain transforma esta clase en un esquema JSON que se envía al LLM. Por lo tanto el modelo lo lee textualmente
def consultar_estado_envio_detallado(numero_seguimiento: str, incluir_historial: bool = False):
    """
    Consulta el estado de un envío con la opción de incluir el historial completo.
    """
    envio = ESTADOS.get(numero_seguimiento)
    if envio is None:
        return f"No se encontró un envío con el número {numero_seguimiento}."

    if not incluir_historial:
        return envio["actual"]

    historial = ", ".join(envio["historial"])
    return f"{envio['actual']}. (Historial: {historial})"

@tool
def calcular_costo_envio(peso_kg: float, distancia_km: float) -> str:
    """
    Calcula el costo estimado de un venío según su peso y la distancia a recorrer. Usa cuando el usuario pregunta cuánto va a costar enviar un producto
    """
    costo = 500 + (peso_kg * 120) + (distancia_km * 3)
    return f"El costo estimado es de ${costo:.2f}"

#Siguiente Tool

#Listado de herramientas
herramientas = [consultar_estado_envio_detallado, calcular_costo_envio]

#Gestión de Historial de Memoria

historiales = {

}

def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()
    return historiales[session_id]

#Construcción del agente, plantilla y ejecutor
prompt_agente = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente de logistica que responde preguntas usando las herramientas disponibles."),
    #Todo: historial de chats
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad")
])

agente = create_tool_calling_agent(modelo, herramientas, prompt_agente)

ejecutor_agente = AgentExecutor(
    agent=agente,
    tools=herramientas,
    verbose=True, #Imprime los pasos que va siguiendo
)

#Agente con memoria - obtener_historial

if __name__ == "__main__":
    resultado = ejecutor_agente.invoke(
        {"entrada": "Cuál es el estado del envío AR12345 incluyendo el historial?"}
    )

    print("Respuesta: ", resultado["output"][0]["text"])



