- **Prompt revision TFM hitos**
    
    Considera que eres un profesor universitario en un Máster de Inteligencia Artificial, y tu tarea es evaluar la memoria técnica del trabajo final de los estudiantes.  Evalua cada uno de los siguientes puntos y da consejos claros para que pueda alcanzar mencion publicacion.
    
    Tu objetivo es:
    
    - **Encontrar errores ortográficos y gramaticales**, y señalar **frases confusas**, indicando en cada caso la **página** donde se encuentran.
    - **Seguir un método de investigación** para evaluar el Trabajo Fin de Máster (TFM) y proporcionar consejos al estudiante en los siguientes puntos:
        - **Introducción**
        - Antecedentes
        - **El Problema**
            - **Situacion Actual**
            - **Formulacion o Planteamiento del problema**
            - Justificacion
            - Delimiacion del Problema
            - **Hipótesis**
            - **Objetivos General**
            - **Objetivos Especificos**
        - **Marco teórico o Contexto Teorico**
        - **Estado del arte**
        - **Materiales y Metodos o Metodología**
            - Planificacion
            - Fases asociadas con el proceso a desarrollar
            - hardware software
        - **Fase de Desarrollo**
            - **Refinamiento de modelos**
        - **Discusión de Resultados o Resultados**
        - **Conclusiones**
        - Futuras lineas de trabajo
        - **Referencias - Explicar que normas sigue (APA o otra) y encontrar errores.**
    
    Tu meta es ayudar al estudiante a adaptar su trabajo para que sea **publicable académicamente**.
    
    - Parte 2.
        
        **A. Calidad de la Investigación:**
        
        1. **Revisión Teórica**: Evaluar la actualidad y exhaustividad de la revisión de la literatura, asegurando que cubra las teorías y modelos relevantes.
        2. **Diseño de la Investigación y Metodología**: Evaluar la alineación del diseño de la investigación y la metodología con los objetivos y preguntas de la investigación.
        3. **Análisis de Datos**: Verificar la exhaustividad del análisis de datos y la precisión de la interpretación de los resultados.
        4. **Integración de Resultados**: Examinar cuán bien se integran los resultados con las teorías establecidas y estudios anteriores.
        5. **Investigación Futura**: Evaluar la profundidad de las perspectivas y las áreas potenciales para futuras investigaciones presentadas en el documento.
        6. **Conexión entre el Estado del Arte y la Discusión de Resultados**: Evalúa cómo se conectan el estado del arte y la discusión de resultados, e indica puntos que el estudiante pueda usar como referencia para mejorar esta conexión.
        7. **Conclusiones**: Evalúa si las conclusiones están bien planteadas y resaltan lo relevante de la investigación.
        8. **Tablas, Figuras y Gráficos**: Evaluar la efectividad de estos elementos para complementar el texto y su correcta referencia.
        9. **Formato de Citas**: Verificar el formato correcto de las citas siguiendo las normas APA dentro del texto y su precisión en correspondencia con la bibliografía.
        
        Tu meta es ayudar al estudiante a adaptar su trabajo para que sea **publicable académicamente**.
        
    - Parte 3.
        
        Encontrar errores ortográficos y gramaticales, y señalar frases confusas, indicando en cada caso la página donde se encuentran.
        
- Parte 4:
    
    Has una revision exahustiva de como el estudiante plantea las metricas de evaluacion del modelo. Si estan acorde para los modelos planteados si falta alguna metrica altamente recomendable. 
    Revisando los resultados de modelo del pdf y las conclusiones, recomienda como seleccionar las metricas para elegir el mejor modelo con estos argumentos
    
    - Promt evaluar metricas
        
        Revisando los resultados de modelo del pdf y las conclusiones, recomienda como seleccionar las metricas para elegir el mejor modelo con estos argumentos
        
        Precisión, Recall, Puntuación F1: ¿Cuál elegir?
        
        Precisión
        Es adecuada cuando es crucial minimizar los falsos positivos, incluso si eso significa omitir algunas instancias positivas.
        Ejemplo: En un clasificador de correos no deseados, una alta precisión garantiza que los correos marcados como spam sean realmente spam, reduciendo las probabilidades de clasificar incorrectamente correos importantes como spam.
        
        Recall (Sensibilidad)
        Es apropiada cuando es vital capturar todas las instancias positivas, incluso si eso implica tolerar algunos falsos positivos.
        Ejemplo: En un sistema de diagnóstico médico, un alto recall asegura que se identifiquen todos los pacientes con una enfermedad, aunque esto conduzca a algunas falsas alarmas.
        
        Puntuación F1
        Es útil cuando se busca un equilibrio entre precisión y recall.
        Ejemplo: En un algoritmo de clasificación de motores de búsqueda, la puntuación F1 puede usarse para evaluar qué tan bien el algoritmo recupera documentos relevantes mientras minimiza los irrelevantes.