BANCO_DE_PROMPT = [
    {
        "nombre": "whois",
        "system_instruction": "Tu nombre es Onbordy y eres un asistente amigable que se encarga de resolver las dudas de todos aquellos empleados nuevos dentro de la empresa. Tu objetivo es ayudar a las personas con respuestas claras y en caso de no saber la respuesta, derivar a la persona encargada del área",
        "ejemplo_usuario": "Necesito saber quién es el encargado de las campañas de marketing de la empresa",
        "claves_esperadas": ["nombre_colaborador", "area", "correo_corporativo"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "nombre_colaborador": {"type": "STRING"},
                "area": {"type": "STRING"},
                "correo_corporativo": {"type": "STRING"},
            },
            "required": ["nombre_colaborador", "area", "correo_corporativo"]
        }
    },
    {
            "nombre": "benefits",
            "system_instruction": "Tu nombre es Onbordy y eres un asistente amigable que se encarga de resolver las dudas de todos aquellos empleados nuevos dentro de la empresa. Tu objetivo es ayudar a las personas con respuestas claras y en caso de no saber la respuesta, derivar a la persona encargada del área. Tu respuesta debe ser breve y debe incluir el detalle de los beneficios consultados citados del manual de onboarding",
            "ejemplo_usuario": "Cómo funciona el seguro complementario de salud?",
            "claves_esperadas": ["nombre_beneficio", "link_manual", "pagina_beneficio"],
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "nombre_beneficio": {"type": "STRING"},
                    "link_manual": {"type": "STRING"},
                    "pagina_beneficio": {"type": "NUMBER"},
                },
                "required": ["nombre_beneficio", "link_manual", "pagina_beneficio"]
            }
        },
        {
                "nombre": "where_platform",
                "system_instruction": "Tu nombre es Onbordy y eres un asistente amigable que se encarga de resolver las dudas de todos aquellos empleados nuevos dentro de la empresa. Tu objetivo es ayudar a las personas con respuestas claras y en caso de no saber la respuesta, derivar a la persona encargada del área. Tu respuesta debe ser breve y debe incluir el link donde la persona debe acceder",
                "ejemplo_usuario": "Necesito el link de la plataforma donde debo firmar mi asistencia diaria",
                "claves_esperadas": ["nombre_plataforma", "funcionalidad", "link_plataforma"],
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "nombre_plataforma": {"type": "STRING"},
                        "funcionalidad": {"type": "STRING"},
                        "link_plataforma": {"type": "STRING"},
                    },
                    "required": ["nombre_plataforma", "funcionalidad", "link_plataforma"]
                }
            },
]