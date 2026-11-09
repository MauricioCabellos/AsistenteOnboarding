# Límites de la métrica de evaluación


## Qué mide

Mide qué tan calcadas son las palabras exactas entre lo que responde el asistente y la respuesta ideal. Se fija en tres cosas:

- **Precisión:** Cuántas palabras de la respuesta del asistente sirvieron y no fueron "paja".
- **Cobertura:** Cuántas palabras de la respuesta ideal alcanzó a mencionar.
- **F1:** La nota final que junta las dos anteriores para ver el balance general.


## Modos de falla conocidos

Al medir solo palabras calcadas, el sistema se equivoca en estos casos:

1) **Falsos castigos por decir lo mismo con otras palabras:** Si el asistente responde bien pero usa sinónimos, el sistema le pone un cero.
    Ejemplo (ID 12): Dijo "se organizan de forma multidisciplinaria" en vez de "células multidisciplinarias". La respuesta era buena, pero sacó F1 = 0.0.
2) **Respuestas a medias que sacan nota:** Si falta información importante pero se usan palabras parecidas, el puntaje no muestra el vacío real.
    Ejemplo (ID 4): Al explicar cómo justificar una licencia médica, no dijo a quién ni en cuántas horas, pero igual sumó puntos (F1 = 0.074).
3) **No detecta respuestas peligrosas o equivocadas:** Si el asistente inventa una regla o se equivoca en un dato, el sistema no lo nota si las palabras suenan parecidas.
    Ejemplo (ID 11): Dio a entender que te puedes conectar a la red de la empresa desde cualquier equipo personal (un riesgo de seguridad), pero sacó mejor nota (F1 = 0.108) que la respuesta bien explicada.
4) **Se le escapan las fechas y los números:** No sabe si un horario o una cifra está bien o mal.
    Ejemplo (ID 1): Se equivocó en el horario de los viernes, pero como embocó casi todas las otras palabras, sacó la nota más alta del grupo (F1 = 0.631).

(ref: docs/revision_manual.json)


## Muestra revisada

10 casos: los 5 con menor F1 y los 5 con mayor F1, sobre 40
respuestas generadas el 2026-08-11.


## Recomendación de uso

- **Usa la nota automática (F1):** Solo para comparar en masa si una versión nueva del asistente habla mejor o peor que la anterior en términos generales.
- **Revisa siempre a mano:** Cuando la pregunta sea sobre reglas estrictas, trámites, canales de ayuda, claves o números. El puntaje automático no sabe si una regla de la empresa es correcta o no, así que la revisión humana sigue siendo indispensable.