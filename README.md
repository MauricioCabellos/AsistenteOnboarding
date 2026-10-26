# Proyecto Asistente Onboarding — Especialización en Desarrollo con IA Generativa (Accenture)

Descripción de la app:


## Requisitos Previos

1) **Python:** 3.10 o superior.
2) **Git:** para clonar el repositorio y gestionar versiones.
3) Gestor de paquetes **pip** actualizado.
4) Accesso a la **APY_KEY** de algún modelo de LLM como **Gemini(recomendado), ChatGPT, Claude o Groq.**


## Instalación

Los siguientes pasos debes hacerlo desde la Terminal:

1. Clona el repositorio de GitHub:
git clone https://github.com/MauricioCabellos/AsistenteOnboarding.git

2. Ingresa a la carpeta:
cd AsistenteOnboarding

3. Crea el entorno virtual:
python3 -m venv venv

4. Activa el entorno virtual:
source venv/bin/activate

5. Instala las dependencias:
pip install -r requirements.txt

6. Copia las variables de entorno y completa las variables según corresponda:
cp .env.example .env

7. Ejecuta la aplicación que verifica el correcto consumo de Gemini:
python3 src/consumir_gemini.py


## Registro de ensayo de instalación limpia

- Fecha: 25-10-2026
- Estado: Problema observado en la instalación
- Encontrado: el archivo '.env.example' no está disponible en el repositorio
- Corregido: se crea el archivo '.env.example' con el detalle de las variables de entorno necesarias.
- Resultado tras la corrección: ya se puede copiar el archivo creando el '.env' como se menciona en la instalación.

------

- Fecha: 25-10-2026
- Estado: Instalación limpia. Se realizan los pasos de instalación en un equipo Apple antiguo (MacBook Pro mid 2014) directamente desde la terminal (sin instalación de VSCode) y el archivo .py corre sin errores.

------
