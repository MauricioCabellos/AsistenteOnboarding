from collections import Counter
from pipeline_limpieza import procesar_texto
from cliente import consultar_modelo
import json
from pathlib import Path


def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)
    
    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

casos = [
    (
        "¿Cuál es el horario laboral de la empresa?",
        "El horario laboral oficial es de lunes a jueves de 9:00 a 18:00 horas, y los viernes de 9:00 a 15:00 horas.",
    ),
    (
        "¿Cuántos días de vacaciones anuales corresponden por contrato?",
        "Corresponden 15 días hábiles de vacaciones anuales tras el primer año cumplido.",
    ),
    (
        "¿Cuál es la política sobre el trabajo remoto o teletrabajo?",
        "La modalidad de trabajo híbrido es de 2 días presenciales y 3 días remotos por semana, según acuerdo con el supervisor.",
    ),
    (
        "¿Cómo se debe justificar una ausencia por enfermedad?",
        "Se debe presentar licencia médica digital a Recursos Humanos dentro de las primeras 48 horas.",
    ),
    (
        "¿Qué cobertura entrega el seguro complementario de salud?",
        "El seguro complementario de salud cubre la diferencia no cubierta por tu previsión de salud.",
    ),
    (
        "¿Cuándo pagan el sueldo?",
        "El pago de remuneraciones se realiza el último día hábil de cada mes.",
    ),
    (
        "¿Existe algún convenio de alimentación para los colaboradores?",
        "Se paga un bono por alimentación todos los meses en tu sueldo.",
    ),
    (
        "¿Qué sistema operativo se utiliza en los equipos corporativos?",
        "Todos los equipos corporativos utilizan macOS o Windows originales, según el rol del colaborador.",
    ),
    (
        "¿Cómo se solicita soporte técnico ante fallas de hardware?",
        "Puedes crear un ticket por llamada telefónica, correo electrónico o WhatsApp de TI.",
    ),
    (
        "¿Qué herramienta se utiliza para la comunicación oficial de equipo?",
        "Todas las comunicaciones oficiales se realizan a través del correo corporativo y redes sociales internas de la empresa.",
    ),
    (
        "¿Cuál es el requisito para conectarse a la red VPN de la empresa?",
        "Todos los equipos proporcionados por la empresa se conectan de forma automática al VPN. Los equipos personales requieren autorización de TI y configuración manual.",
    ),
    (
        "¿Cómo se estructuran los equipos de trabajo en la compañía?",
        "Los equipos operan bajo metodologías ágiles divididos en células multidisciplinarias autónomas.",
    ),
    (
        "¿A qué área se debe reportar cualquier conflicto laboral?",
        "Cualquier conflicto laboral, ya sea hacia ti o que hayas presenciado, debe reportarse directamente al canal de denuncias anónimo.",
    ),
    (
        "¿Cada cuánto tiempo se realizan las evaluaciones de desempeño?",
        "Las evaluaciones de desempeño se realizan anualmente. Consta de 3 etapas: 1) Defición de objetivos, 2) Autoevaluación y 3) Retroalimentación y Entrega de resultados.",
    ),
    (
        "¿Dónde se encuentran los documentos oficiales de procesos internos?",
        "Los documentos oficiales se encuentran en la plataforma ARIS de la empresa.",
    ),
    (
        "¿Cuál es la política sobre el uso de contraseñas seguras?",
        "Las contraseñas deben tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y símbolos. Éstas deben cambiarse cada 90 días.",
    ),
    (
        "¿Se permite compartir credenciales de acceso corporativas con terceros?",
        "Está estrictamente prohibido compartir credenciales de acceso corporativas con cualquier persona ajena a la empresa. El incumplimiento puede resultar en sanciones disciplinarias.",
    ),
    (
        "¿Cómo se deben manejar los datos sensibles de los clientes?",
        "Los datos sensibles deben manejarse bajo estrictos protocolos de anonimización y encriptación. Todo acceso a la base de datos debe registrarse y auditarse. El incumplimiento puede resultar en sanciones disciplinarias.",
    ),
    (
        "¿Qué se debe hacer en caso de sospecha de brecha de seguridad?",
        "Se debe notificar de inmediato al equipo de ciberseguridad a través del canal de reporte.",
    ),
    (
        "¿Cada cuánto tiempo se debe actualizar la contraseña de acceso al sistema?",
        "Las contraseñas deben actualizarse cada 90 días y no deben reutilizarse las últimas 4 contraseñas.",
    ),
]

raiz = Path(__file__).resolve().parents[1]
ruta_resultados = raiz / "docs" / "resultados_metricas.json"

# Recupera las respuestas guardadas en una ejecución anterior.
if ruta_resultados.exists():
    with ruta_resultados.open(
        "r",
        encoding="utf-8"
    ) as archivo:
        resultados = json.load(archivo)
else:
    resultados = []

# Identifica los casos ya completados.
completados = {
    (caso["consulta"], caso["referencia"])
    for caso in resultados
}

for numero, (consulta, referencia) in enumerate(
    casos,
    start=1
):
    # Continúa sin repetir las consultas ya guardadas.
    if (consulta, referencia) in completados:
        print("Ya guardada:", consulta)
        continue

    try:
        respuesta = consultar_modelo(
            consulta,
            system_instruction=(
                "Responde en español con una definición breve, "
                "en una sola oración de máximo 15 palabras. "
                "Sin listas, ejemplos ni introducciones."
            )
        )

    except RuntimeError as error:
        print("\nSe detuvo la generación:", error)
        print(f"Respuestas guardadas: {len(resultados)}")
        break

    metricas = calcular_metricas(referencia, respuesta)

    resultados.append({
        "id": numero,
        "consulta": consulta,
        "referencia": referencia,
        "respuesta": respuesta,
        **metricas,
    })

    # Guarda inmediatamente después de cada respuesta.
    with ruta_resultados.open(
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            resultados,
            archivo,
            indent=2,
            ensure_ascii=False
        )

    completados.add((consulta, referencia))

    print("\nConsulta:", consulta)
    print("Respuesta:", respuesta)
    print("Métricas:", metricas)
    print(f"Guardadas: {len(resultados)}/{len(casos)}")

def resumir_metricas(resultados):
    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }
    n = len(resultados)
    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,
        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,
        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }
    
print("Promedios")
print(resumir_metricas(resultados))
    
peores_casos = sorted(resultados, key=lambda r: r["f1"])

for caso in peores_casos[:3]:
    print(caso["consulta"], caso["f1"])
    
    
# referencia = procesar_texto(
#     "Python es un lenguaje de programación interpretado."
# )

# texto_respuesta = consultar_modelo("¿Qué es Python?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)