# Límites de la métrica de evaluación


## Qué mide

Coincidencia de palabras entre una respuesta generada y una
referencia, contando repeticiones (precisión, cobertura, F1).
(una frase: qué compara la métrica y qué cuenta)


## Modos de falla conocidos

- Sinónimos y paráfrasis correctas puntúan bajo (ver ejemplo
  en docs/).
- Datos incorrectos (fechas, cifras) pueden puntuar alto si el
  resto de la oración coincide.
- Negaciones ausentes casi no bajan el puntaje, aunque
  inviertan el significado.
(una viñeta por casom con un ejemplo concreto de cada uno)


## Muestra revisada

10 casos: los 5 con menor F1 y los 5 con mayor F1, sobre 40
respuestas generadas el 2026-08-10.
(cuántos casos revisaste a mano y cómo los elegiste, recomendado 5 mejores y 5 peores)


## Recomendación de uso

Usar F1 para comparar en volumen entre versiones del cliente.
Revisar siempre a mano cualquier respuesta con fechas, cifras
o nombres propios.
(cuándo confiar en el número solo y cuándo revisar a mano)